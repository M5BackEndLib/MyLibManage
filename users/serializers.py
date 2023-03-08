from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "password",
            "avatar_url",
            "is_blocked",
            "is_employee",
        ]
        read_only_fields = ["id", "is_blocked"]
        extra_kwargs = {"password": {"write_only": True}}


class Token(TokenObtainPairSerializer):
    def get_token(cls, data):
        vereify_superuser = super().get_token(data)
        vereify_superuser["is_superuser"] = data.is_superuser

        return vereify_superuser
