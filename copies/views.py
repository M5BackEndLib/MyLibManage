from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from datetime import datetime
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly
from rest_framework import serializers
from .models import Copy, CopyLoan
from .serializers import CopyLoanSerializer, CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
        book_find = get_object_or_404(Book, pk=self.kwargs["book_id"])
        serializer.save(book=book_find)


class CopyLoanCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CopyLoan.objects.all()
    serializer_class = CopyLoanSerializer

    def perform_create(self, serializer):
        copy_id = self.kwargs.get("id")
        copy = get_object_or_404(Copy, id=copy_id)
        serializer.save(user=self.request.user, copy=copy)


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
    permission_classes = [IsAuthenticated]
    serializer_class = CopyLoanSerializer
    queryset = CopyLoan.objects.all()

    def put(self, request, *args, **kwargs):
        user = request.user
        copy_id = kwargs.get("id")
        copy_loan = CopyLoan.objects.filter(
            copy__id=copy_id, user=user, returned=False
        ).first()
        print(CopyLoan.objects.all())
        print(copy_id)
        if copy_loan is None:
            return Response(
                {"detail": "You don't have a loan on this copy."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_blocked:
            user.is_blocked = False
            user.save()

        copy_loan.returned = True
        copy_loan.returned_in = datetime.now()
        copy_loan.save()

        copy = copy_loan.copy
        copy.disponibility = True
        copy.save()

        return Response(
            {"detail": "Livro retornado com sucesso."}, status=status.HTTP_200_OK
        )
