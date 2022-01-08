import json
import bcrypt
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from django.views import View
from users.models import User
from account.models import Account
from transaction.models import Transaction
from transaction.helper import update_account, create_transaction, check_auth, trade, AccountAuthError, BalanceError
from transaction.validators import validate_amount, validate_description, validate_account_number, validate_t_type, validate_end_date, validate_start_date, validate_list_t_type
from users.utils import login_decorator
from django.core.exceptions import ValidationError
from transaction.constant import DEPOSIT, WITHDRAW


class DepositView(View):
    '''
    입금을 도맡아 진행하는 클래스 뷰입니다.
    클라이언트로 부터 계좌번호, 입금 금액, 적요를 입력받습니다.
    계좌가 존재하고 소유주가 맞는지 확인합니다.
    '''
    @login_decorator
    def post(self, request):
        try:
            # 데이터 검증
            data = json.loads(request.body)
            user = request.user
            account_number = validate_account_number(data['account_number'])
            deposit_amount = validate_amount(data['amount'])
            description = validate_description(data['description'])

            # 계좌 존재 확인
            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            # 권한 확인
            account = check_auth(user, account_number)

            # 입금 실행
            transaction_result = trade(
                account, deposit_amount, description, DEPOSIT)

            # 응답 데이터 생성
            data = obj_to_data(transaction_result)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)

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
        try:
            data = json.loads(request.body)
            account_number = validate_account_number(data['account_number'])
            withdraw_amount = validate_amount(data['amount'])
            description = validate_description(data['description'])
            user = request.user

            # 계좌 존재 확인
            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            # 거래 권한 확인
            account = check_auth(user, account_number)

            # 거래 가능 확인
            if account.balance < withdraw_amount:
                raise BalanceError

            # 출금 실행
            transaction_result = trade(
                account, withdraw_amount, description, WITHDRAW)

            # 응답 데이터 생성
            data = obj_to_data(transaction_result)
            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)
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
    def get(self, request):
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

            # 해당 계좌가 존재하는지 확인
            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            # 해당 계좌의 소유주가 맞는지 확인
            account = check_auth(user, account_number)

            # 필터링
            filters = self.transaction_list_filter(
                account, started_date, end_date, transaction_type)

            # 리스트 갯수
            list_count = Transaction.objects.filter(**filters).count()

            # 거래 내역 조회
            transaction_list = Transaction.objects.filter(
                **filters).order_by("id")[offset:limit]

            # 데이터 변환
            results = self.obj_to_list(transaction_list, account)
            return JsonResponse({'Message': 'SUCCESS', 'Data': results, 'TotalCount': list_count}, status=200)

        # 계좌 권한 없는 경우
        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        # 검증 에러
        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)

    # 데이터 필터링 함수
    def transaction_list_filter(self, account, start_date, end_date, transaction_type):
        '''
        필터링 조건에 맞게 딕셔너리를 생성합니다.
        '''
        filters = {'account': account}

        if transaction_type == WITHDRAW:
            filters['transaction_type'] = WITHDRAW
        elif transaction_type == DEPOSIT:
            filters['transaction_type'] = DEPOSIT

        if start_date and end_date:
            filters['created_at__gte'] = start_date
            filters['created_at__lt'] = end_date

        return filters

    # 데이터 변환
    def obj_to_list(self, transaction_list: Transaction, account: Account):
        results = [{
            '계좌 번호': account.account_number,
            '거래 후 잔액': transaction.balance,
            '금액': transaction.amount,
            '적요': transaction.description,
            '거래 종류': transaction.transaction_type,
            '거래 일시': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }for transaction in transaction_list]

        return results


def obj_to_data(transaction_history: Transaction):
    data = {
        "거래 계좌": transaction_history.account.account_number,
        "거래 금액": transaction_history.amount,
        "거래 후 금액": transaction_history.balance,
        "거래 종류": transaction_history.transaction_type,
        "거래 날짜": transaction_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "적요": transaction_history.description
    }

    return data


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
