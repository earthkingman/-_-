from django.db import models
from account.models import Account
from .validators import validate_amount, validate_balance, validate_t_type

# Create your models here.


class Transaction(models.Model):
    account = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField(
        null=False, validators=[validate_balance])
    amount = models.PositiveBigIntegerField(
        null=False, validators=[validate_amount])
    transaction_type = models.CharField(max_length=2, null=False,
                                        validators=[validate_t_type])
    description = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_history'
        indexes = [
            models.Index(fields=['account_id', 'transaction_type']),
            models.Index(fields=['account_id', 'created_at']),
        ]
