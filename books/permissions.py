from rest_framework import permissions
from .models import User
from rest_framework.views import View

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_employee or request.method in SAFE_METHODS