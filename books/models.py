from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=30, unique=True)
    author = models.CharField(max_length=50)
    cover = models.CharField(max_length=255)
    synopsis = models.CharField(max_length=155)
    status = models.BooleanField()
    follows = models.ManyToManyField("Users.user", related_name="follow_books")
