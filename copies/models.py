from django.db import models
import uuid

# Create your models here.
class Copy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    added_in = models.DateField(auto_now=True)
    book = models.ForeignKey(
        "Books.book", on_delete=models.CASCADE, related_name="copies"
    )
