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


class Trade:
  
    def update_account(self, withdraw_amount, ex_account):
        ex_account.balance = ex_account.balance - withdraw_amount
        ex_account.save()
        return ex_account

    def create_transaction(self, withdraw_amount, description, ex_account, t_type):
        transaction_history = Transaction.objects.create(
            account = ex_account,
            amount = withdraw_amount,
            balance = ex_account.balance,
            t_type = t_type,
            description = description
        )
        return transaction_history

    def check_exit(self, authenticated_user, account_number):
            # get_object_or_404() 사용한 방법
            # ex_account = get_object_or_404(Account, account_number = account_number)
            # auth = get_object_or_404(Account, account_number = account_number, user = authenticated_user)
            try:
                ex_account = Account.objects.get(account_number = account_number)
            except Account.DoesNotExist:
                return False
        
    def check_auth(self, authenticated_user, account_number):
            try:
                ex_account = Account.objects.get(account_number = account_number, user = authenticated_user)
                return ex_account
            except Account.DoesNotExist:
                return False


class DepositView(View, Trade):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            deposit_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if super().check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIT_ERROR'},status=400)

            ex_account = super().check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
                
            self.deposit(ex_account, deposit_amount, description)
            return JsonResponse({'Message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400) 
    
    @transaction.atomic
    def deposit(self, ex_account, deposit_amount, description):
    
        amount_after_transaction = super().update_account(deposit_amount, ex_account) #해당 계좌 잔액 수정

        transaction_history = super().create_transaction(deposit_amount, description, ex_account, "입금") #거래 내역 생성
        
        return amount_after_transaction, transaction_history

class WithdrawView(View, Trade):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            withdraw_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if super().check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIT_ERROR'},status=400)

            ex_account = super().check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
                
            self.withdraw(ex_account, withdraw_amount, description)
            return JsonResponse({'Message':'SUCCESS'},status=201)
            
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400)

    @transaction.atomic
    def withdraw(self, ex_account, withdraw_amount, description):

        amount_after_transaction = super().update_account(withdraw_amount, ex_account) #해당 계좌 잔액 수정

        transaction_history = super().create_transaction(withdraw_amount, description, ex_account, "출금") #거래 내역 생성
        
        #return amount_after_transaction, transaction_history



