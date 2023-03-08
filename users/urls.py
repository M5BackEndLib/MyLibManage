from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
    path("users/", UserView.as_view()),
]
