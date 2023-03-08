from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly
from .models import Copy
from .serializers import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.
class CopyView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployeeOrReadOnly]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book_find = get_object_or_404(Book, pk=self.kwargs["book_id"])
        serializer.save(book=book_find)
