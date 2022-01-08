import json
from django.views import View
from django.http import JsonResponse
# from transaction.helper import update_account, create_transaction, check_auth, trade, AccountAuthError
from users.utils import login_decorator
from account.models import Account
# from transaction.helper import trade
from users.models import User
from json.decoder import JSONDecodeError
from transaction.validators import validate_amount, validate_account_number
from transaction.constant import DEPOSIT, DESCRIPTION

# Create your views here.


class AccountView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            # 데이터 검증
            deposit_amount = validate_amount(data['amount'])
            account_number = validate_account_number(data['account_number'])

            # 계좌 존재 확인
            if Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)

            # 계좌 생성
            account = Account.objects.create(
                user=user,
                account_number=account_number,
                balance=0
            )
            # 기본 금액 입금
            data = trade(account, deposit_amount, DESCRIPTION, DEPOSIT)
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        try:
            # 데이터 검증
            user = request.user
            account_number = validate_account_number(
                request.GET.get("account_number", None))

            # 계좌 존재 확인
            account = Account.objects.filter(account_number=account_number)

            # 응답 값 생성
            data = {
                "계좌 번호": account[0].account_number,
                "소유주 ": account[0].user.email,
                "잔액": account[0].balance,
            }
            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=200)

        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)
