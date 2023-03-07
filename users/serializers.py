from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "avatar_url", "is_blocked", "is_employee"]

class Token(TokenObtainPairSerializer):
    def get_token(cls, data):
        vereify_superuser = super().get_token(data)
        vereify_superuser["is_superuser"] = data.is_superuser

        return vereify_superuser
