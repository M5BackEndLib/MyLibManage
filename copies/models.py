from django.db import models

# Create your models here.
class Copy(models.Model):
    added_in = models.DateField(auto_now=True)
    book = models.ForeignKey(
        "Books.book", on_delete=models.CASCADE, related_name="copies"
    )
