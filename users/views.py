from django.shortcuts import render
from .serializers import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import UserSerializer
from .models import User

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class LoginView(TokenObtainPairView):
    token_serializer = Token
