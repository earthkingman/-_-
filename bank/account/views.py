import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
# Where절에 Or 문을 추가하고 싶다면 사용
from transaction.helper import update_account, create_transaction, check_auth, trade, AccountAuthError, TransactionTypeError
# from users.utils import login_decorator
from account.models import Account
from transaction.helper import trade
from users.models import User
from json.decoder import JSONDecodeError
from transaction.validators import validate_amount, validate_account_number
# Create your views here.


class AccountView(View):
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            # userId = request.user
            user_id = request.session['userId']
            deposit_amount = validate_amount(data['amount'])
            account_number = validate_account_number(data['account_number'])

            if Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)
            user = User.objects.get(id=user_id)
            account = Account.objects.create(
                user=user,
                account_number=account_number,
                balance=0
            )
            if deposit_amount > 0:
                data = trade(account, deposit_amount, "계좌생성", "입금")
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
