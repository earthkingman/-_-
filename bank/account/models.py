from django.db import models
from users.models import User
from .validators import validate_balance
# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, null=False, unique=True)
    balance = models.PositiveBigIntegerField(
        null=False, validators=[validate_balance])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
