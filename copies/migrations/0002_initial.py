# Generated by Django 4.1.7 on 2023-03-08 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('copies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyloan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_loan_copies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='copy',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='books.book'),
        ),
        migrations.AddField(
            model_name='copy',
            name='loans',
            field=models.ManyToManyField(related_name='loans_copies', through='copies.CopyLoan', to=settings.AUTH_USER_MODEL),
        ),
    ]