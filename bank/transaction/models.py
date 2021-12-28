from django.db import models
from account.models import Account

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField()
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)