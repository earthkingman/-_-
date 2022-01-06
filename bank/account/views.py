import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from django.db.models import Q  # Where절에 Or 문을 추가하고 싶다면 사용

from users.utils import login_decorator
from account.models import Account
from transaction.helper import trade
from users.models import User


# Create your views here.
class AccountView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            if Account.objects.filter(account_number=data['account']).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)

            account = Account.objects.create(
                user=user,
                account_number=data['account'],
                balance=0
            )
            deposit_amount = account_number = data['balance']
            data = trade(account, deposit_amount, "계좌생성", "입금")
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except ValueError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
