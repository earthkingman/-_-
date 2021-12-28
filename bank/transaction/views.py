import json
from datetime import datetime, timedelta
from django.http  import JsonResponse
from django.views import View
from django.db import transaction
from users.models import User
from account.models import Account
from transaction.models import Transaction

from django.shortcuts import render, get_object_or_404
from users.utils      import login_decorator
# Create your views here.

class DepositView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            deposit_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIT_ERROR'},status=400)

            ex_account = check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
                
            self.deposit(ex_account, deposit_amount, description)
            return JsonResponse({'Message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400) 
    
    @transaction.atomic
    def deposit(self, ex_account, deposit_amount, description):
    
        amount_after_transaction = self.update_account(deposit_amount, ex_account) #해당 계좌 잔액 수정

        transaction_history = self.create_transaction(deposit_amount, description, ex_account) #거래 내역 생성
        
        return amount_after_transaction, transaction_history

    def update_account(self, deposit_amount, ex_account):
        ex_account.balance = ex_account.balance + deposit_amount
        ex_account.save()
        return ex_account

    def create_transaction(self, deposit_amount, description, ex_account):
        transaction_history = Transaction.objects.create(
            account = ex_account,
            amount = deposit_amount,
            balance = ex_account.balance,
            t_type = "입금",
            description = description
        )
        return transaction_history

class WithdrawView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            withdraw_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIT_ERROR'},status=400)

            ex_account = check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
                
            self.withdraw(ex_account, withdraw_amount, description)
            return JsonResponse({'Message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400) 


def check_exit(authenticated_user, account_number):
        # get_object_or_404() 사용한 방법
        # ex_account = get_object_or_404(Account, account_number = account_number)
        # auth = get_object_or_404(Account, account_number = account_number, user = authenticated_user)
        try:
            ex_account = Account.objects.get(account_number = account_number)
        except Account.DoesNotExist:
            return False
    
def check_auth(authenticated_user, account_number):
        try:
            ex_account = Account.objects.get(account_number = account_number, user = authenticated_user)
            return ex_account
        except Account.DoesNotExist:
            return False


        

