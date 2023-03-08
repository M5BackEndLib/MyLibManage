from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.CharField(max_length=150, unique=True, null=False)
    phone = models.CharField(max_length=50, unique=True)
    avatar_url = models.CharField(max_length=255)
    is_blocked = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
