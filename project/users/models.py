from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(unique=True, null=False, max_length=50)
    password = models.CharField(null=False, max_length=50)
    refresh_token = models.CharField(max_length=300, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
