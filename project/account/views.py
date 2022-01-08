import json
from django.views import View
from django.http import JsonResponse
from users.utils import login_decorator
from account.models import Account
from users.models import User
from json.decoder import JSONDecodeError
from transaction.validators import validate_amount, validate_account_number
from transaction.constant import DESCRIPTION
from account.serivce import AccountService
from transaction.service import TransactionService


class AccountView(View):
    @login_decorator
    def post(self, request) -> JsonResponse:
        account_service: AccountService = AccountService()
        transaction_service: TransactionService = TransactionService()
        try:
            data = json.loads(request.body)
            user: User = request.user

            # 데이터 검증
            deposit_amount: int = validate_amount(data['amount'])
            account_number: str = validate_account_number(
                data['account_number'])

            # 계좌 존재 확인
            if Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)

            # 계좌 생성
            account: Account = account_service.create_account(
                user, account_number)

            # 기본 금액 입금
            transaction_service.deposit(account, deposit_amount, DESCRIPTION)
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)

    @login_decorator
    def get(self, request) -> JsonResponse:
        account_service: AccountService = AccountService()
        try:
            # 데이터 검증
            user: User = request.user
            account_number: str = validate_account_number(
                request.GET.get("account_number", None))

            # 계좌 존재 확인
            data: dict = account_service.select_account(
                account_number=account_number)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=200)

        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)
