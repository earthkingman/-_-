from datetime import datetime, timedelta
from django.http  import JsonResponse
from users.models import User
from transaction.models import Transaction
from django.shortcuts import render
from users.utils      import login_decorator
# Create your views here.

    @login_decorator
    @transaction.atomic
    def deposit(self, authenticated_member: Member, account_number: str, deal_amount: int, description: str) -> Tuple[int, DealHistory]:
        found_account = Account.objects.get(account_number=account_number)

        self.__check_is_account_owner(authenticated_member, found_account)

        result_balance = self.__update_account_balance(deal_amount, found_account, DealHistory.DealType.DEPOSIT)

        created_deal_history = self.__create_deal_history(deal_amount, description, found_account, result_balance, DealHistory.DealType.DEPOSIT)
        
        return result_balance, created_deal_history


    def _check_is_account_owner:
