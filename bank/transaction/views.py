import json, bcrypt
from datetime import datetime, timedelta
from django.http  import JsonResponse
from django.views import View
# from django.db import transaction
from users.models import User
from account.models import Account
from transaction.models import Transaction

from transaction.tradeClass import Trade
from django.shortcuts import render, get_object_or_404
from users.utils      import login_decorator
# Create your views here.

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
                
            super().trade(ex_account, deposit_amount, description, t_type)
            return JsonResponse({'Message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400) 
    
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
                
            super().trade(ex_account, withdraw_amount , description, t_type)
            return JsonResponse({'Message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400)

 
class SeedView(View, Trade):
    def post(self, request):
        try :
            for i in range(1, 11):
                user = User.objects.create(
                    email        = "test" + str(i) + "@8Percent.com",
                    password     = bcrypt.hashpw("1234".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
                    )
                account = Account.objects.create(
                    user = user,
                    account_number = "계좌" + str(i),
                    balance = 1000
                )
                for j in range(1, 20):
                    super().trade(account, 100 , "월급", "입금")
                    super().trade(account, 50 , "카드값", "출금")
            return JsonResponse({'Message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'Message':'KEY_ERROR'},status=400)
