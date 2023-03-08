from django.shortcuts import render
from rest_framework import generics
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly
from books.serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployeeOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, obj=self.request.user)
        serializer.save()
