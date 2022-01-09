import json
import bcrypt
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from django.views import View
from users.models import User
from account.models import Account
from transaction.models import Transaction
# from transaction.helper import update_account, create_transaction, check_auth, trade, AccountAuthError, BalanceError
from transaction.validators import validate_amount, validate_description, validate_account_number, validate_t_type, validate_end_date, validate_start_date, validate_list_t_type
from users.utils import login_decorator
from django.core.exceptions import ValidationError
from transaction.constant import DEPOSIT, WITHDRAW
from transaction.service import TransactionService, ExitsError, AccountAuthError, BalanceError


class DepositView(View):
    '''
    입금을 도맡아 진행하는 클래스 뷰입니다.
    클라이언트로 부터 계좌번호, 입금 금액, 적요를 입력받습니다.
    계좌가 존재하고 소유주가 맞는지 확인합니다.
    '''
    @login_decorator
    def post(self, request):
        transcation: TransactionService = TransactionService()
        try:
            # 데이터 검증
            data = json.loads(request.body)
            user: User = request.user
            account_number: str = validate_account_number(
                data['account_number'])
            deposit_amount: int = validate_amount(data['amount'])
            description: str = validate_description(data['description'])

            # 계좌 존재 및 권한 존재 확인
            account: Account = transcation.check_auth(user, account_number)

            # 입금 실행
            transaction_result: dict = transcation.deposit(
                account, deposit_amount, description)

            return JsonResponse({'Message': 'SUCCESS', "Data": transaction_result}, status=201)

        except ExitsError:
            return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)
        except ValidationError as detail:  # 검증 에러
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)
        except AccountAuthError:  # 권한 에러
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:  # json.loads 에러
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)


class WithdrawView(View):
    '''
    출금을 도맡아 진행하는 클래스 뷰입니다.
    클라이언트로 부터 계좌번호, 입금 금액, 적요를 입력받습니다.
    계좌가 존재하고 소유주가 맞는지 확인합니다.
    거래가 시작되기 전에 출금이 가능한지 먼저 확인합니다.
    '''
    @login_decorator
    def post(self, request):
        transcation: TransactionService = TransactionService()
        try:
            data = json.loads(request.body)
            account_number: str = validate_account_number(
                data['account_number'])
            withdraw_amount: int = validate_amount(data['amount'])
            description: str = validate_description(data['description'])
            user: User = request.user

            # 계좌 존재 및 권한 확인
            account: Account = transcation.check_auth(user, account_number)

            # 거래 가능 확인
            if account.balance < withdraw_amount:
                raise BalanceError

            # 출금 실행
            transaction_result: dict = transcation.withdraw(
                account, withdraw_amount, description)

            return JsonResponse({'Message': 'SUCCESS', "Data": transaction_result}, status=201)

        except ExitsError:
            return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)
        # 값이 안들어오는 경우
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)

        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)

        except BalanceError:
            return JsonResponse({'Message': 'BALANCE_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)


class ListView(View):
    '''
    거래 내역을 조회합니다.
    계좌 번호와 필터링 조건(날짜, 거래 종류)들을 입력받습니다.
    계좌가 존재하고 소유주가 맞는지 확인합니다.
    '''
    @login_decorator  # 해당 계좌, 페이지
    def get(self, request) -> JsonResponse:
        trasaction_service: TransactionService = TransactionService()
        try:
            user = request.user
            account_number = validate_account_number(
                request.GET.get("account_number", None))
            transaction_type = validate_list_t_type(
                request.GET.get("transaction_type", None))
            started_date = validate_start_date(
                request.GET.get("started_at", None))
            end_date = validate_end_date(request.GET.get("end_at", None))
            offset = int(request.GET.get("offset", 0))
            limit = int(request.GET.get("limit", 10))

            # 해당 계좌의 존재하는지 소유주가 맞는지 확인
            account: Account = trasaction_service.check_auth(
                user, account_number)

            data = trasaction_service.get_transaction_list(
                account, started_date, end_date, transaction_type, offset, limit)
            return JsonResponse({'Message': 'SUCCESS', 'Data': data, 'TotalCount': 2}, status=200)

        # 계좌 존재하지 않는 경우
        except ExitsError:
            return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)
        # 계좌 권한 없는 경우
        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        # 검증 에러
        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)


# class SeedView(View):
#     def post(self, request):
#         try:
#             for i in range(1, 11):
#                 user = User.objects.create(
#                     email="test" + str(i) + "@8Percent.com",
#                     password=bcrypt.hashpw("1234".encode(
#                         'utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 )
#                 account = Account.objects.create(
#                     user=user,
#                     account_number="계좌" + str(i),
#                     balance=1000
#                 )
#             account = Account.objects.get(account_number="계좌1")
#             for j in range(1, 300000):
#                 print(j)
#                 trade(account, 100, "월급", "입금")
#                 trade(account, 50, "카드값", "출금")
#                 trade(account, 30, "비트코인", "출금")
#                 trade(account, 5, "햄버거", "출금")
#                 trade(account, 5, "피자", "출금")
#             return JsonResponse({'Message': 'SUCCESS'}, status=200)
#         except KeyError:
#             return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
