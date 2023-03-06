from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class Token(TokenObtainPairSerializer):
    def get_token(cls, data):
        vereify_superuser = super().get_token(data)
        vereify_superuser["is_superuser"] = data.is_superuser

        return vereify_superuser
