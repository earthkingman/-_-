from django.db import models

# Create your models here.
class Withdraw(models.Model):
    id = models.IntegerField
    new_balance = models.PositiveBigIntegerField
    old_balance = models.PositiveBigIntegerField
    amount = models.PositiveBigIntegerField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)