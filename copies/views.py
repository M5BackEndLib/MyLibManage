from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from datetime import datetime
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly
from rest_framework import serializers
from users.models import User
from .models import Copy, CopyLoan
from .serializers import CopyLoanSerializer, CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.mail import send_mass_mail, send_mail
import ipdb


# Create your views here.
class CopyView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployeeOrReadOnly]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        book = self.kwargs["book_id"]
        return Copy.objects.filter(book_id=book)

    def perform_create(self, serializer):
        self.check_object_permissions(obj=self.request.user, request=self.request)
        book_find = get_object_or_404(Book, pk=self.kwargs["book_id"])
        serializer.save(book=book_find)


class CopyLoanCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrReadOnly]
    queryset = CopyLoan.objects.all()
    serializer_class = CopyLoanSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(obj=self.request.user, request=self.request)
        copy_id = self.kwargs.get("copy_id")
        copy = get_object_or_404(Copy, id=copy_id)
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        if user.is_blocked:
            return Response({"detail": "user is blocked"}, 404)
        serializer.save(user=user, copy=copy)


class UserLoanListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CopyLoanSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.user_loan_copies.all()
        return queryset


class ReturnCopyView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrReadOnly]
    serializer_class = CopyLoanSerializer
    queryset = CopyLoan.objects.all()

    lookup_url_kwarg = "loan_id"

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(obj=request.user, request=request)
        copy_id = kwargs.get("loan_id")
        copy_loan = CopyLoan.objects.filter(copy__id=copy_id, returned=False).first()

        if copy_loan is None:
            return Response(
                {"detail": "You don't have a loan on this copy."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=copy_loan.user.id)
        if user.is_blocked:
            user.is_blocked = False
            user.save()

        copy_loan.returned = True
        copy_loan.returned_in = datetime.now()
        copy_loan.save()

        copy = copy_loan.copy
        copy.disponibility = True
        copy.save()

        # signaling followers
        book = copy.book
        mail_list = []
        for user in book.follows.all():
            mail_list.append(user.email)
        send_mail(
            subject="Book Copy Available",
            message=f"Hello! One copy of the book {book.title} is available now.",
            from_email=settings.EMAIL_HOST,
            recipient_list=mail_list,
            fail_silently=False,
        )

        return Response(
            {"detail": "Livro retornado com sucesso."}, status=status.HTTP_200_OK
        )
