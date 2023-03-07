from django.shortcuts import render
from rest_framework import generics
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly
from books.serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Create your views here.
class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
