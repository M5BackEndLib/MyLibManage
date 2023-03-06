from django.shortcuts import render
from .serializers import Token
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    token_serializer = Token
