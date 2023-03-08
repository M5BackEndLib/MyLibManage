from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "synopsis"]
        read_only_fields = ["id"]
