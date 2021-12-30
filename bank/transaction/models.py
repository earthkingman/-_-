from django.db import models
from account.models import Account

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField()
    amount = models.PositiveBigIntegerField()
    t_type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_index_history'
        indexes = [
            models.Index(fields=['account_id', 't_type']),
            models.Index(fields=['account_id', 'created_at']),
        ]