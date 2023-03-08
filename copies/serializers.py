from rest_framework import serializers
from .models import Copy


class CopySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="book.title")

    class Meta:
        model = Copy
        fields = [
            "id",
            "name",
            "book_id",
            "added_in",
            "disponibility",
        ]
        read_only_fields = ["id", "added_in", "book_id", "disponibility"]
