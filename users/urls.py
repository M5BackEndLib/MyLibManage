from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BiblioteKA",
      default_version='v1',
      description="API de Biblioteka, Grupo 37 - Kenzie Academy",
      contact=openapi.Contact(email="teste@teste.com"),
      license=openapi.License(name="Grupo37"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
    path("users/", UserView.as_view()),
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
