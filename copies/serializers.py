from rest_framework import serializers

from .models import Copy

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id","added_in", "book"]
        read_only_fields = ["id"]
