from django.db import models
import uuid
from django.utils import timezone


class Copy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    added_in = models.DateField(auto_now=True)
    book = models.ForeignKey(
        "Books.book", on_delete=models.CASCADE, related_name="copies"
    )
    loans = models.ManyToManyField("User", related_name="users")


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_in = models.DateTimeField(default=timezone.now)
    returned = models.BooleanField(default=False)
    returned_in = models.DateTimeField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )
    copy = models.ForeignKey(
        "copies.Copy",
        on_delete=models.CASCADE
    )
