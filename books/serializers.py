from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "synopsis", "status", "follows"]
        read_only_fields = ["id", "status"]
