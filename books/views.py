from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from books.models import Book
from books.permissions import IsEmployeeOrReadOnly, IsNotEmployee
from books.serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound

# Create your views here.
class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployeeOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, obj=self.request.user)
        serializer.save()


class FollowView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsNotEmployee]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_url_kwarg = "book_id"

    def get_object(self):
        self.check_object_permissions(self.request, obj=self.request.user)
        book_id = self.kwargs["book_id"]
        book_find = get_object_or_404(Book, id=book_id)

        if not book_find:
            raise NotFound("book not found")

        book_find.follows.add(self.request.user)

        return book_find
