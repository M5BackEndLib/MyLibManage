from django.urls import path
from rest_framework_simplejwt import TokenRefreshView
from views import LoginView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
]
