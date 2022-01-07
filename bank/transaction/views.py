import json
import bcrypt
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from django.views import View
from users.models import User
from account.models import Account
from transaction.models import Transaction
from transaction.helper import update_account, create_transaction, check_auth, trade, AccountAuthError, BalanceError, TransactionTypeError
from transaction.validators import validate_amount, validate_description, validate_account_number, validate_t_type, validate_end_date, validate_start_date, validate_list_t_type
# from users.utils import login_decorator
from django.core.exceptions import ValidationError


class DepositView(View):
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            user_id = request.session['userId']
            account_number = validate_account_number(data['account_number'])
            deposit_amount = validate_amount(data['amount'])
            description = validate_description(data['description'])
            t_type = validate_t_type(data['t_type'])

            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            ex_account = check_auth(user_id, account_number)

            data = trade(ex_account, deposit_amount, description, t_type)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)
        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class WithdrawView(View):
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.session['userId']
            account_number = validate_account_number(data['account_number'])
            withdraw_amount = validate_amount(data['amount'])
            description = validate_description(data['description'])
            t_type = validate_t_type(data['t_type'])

            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            ex_account = check_auth(user_id, account_number)
            if ex_account.balance - withdraw_amount < 0:
                raise BalanceError
            data = trade(ex_account, withdraw_amount, description, t_type)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)
        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        except BalanceError:
            return JsonResponse({'Message': 'BALANCE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class ListView(View):
    # @login_decorator  # 해당 계좌, 페이지
    def get(self, request):
        try:
            user_id = request.session['userId']
            account_number = validate_account_number(
                request.GET.get("account_number", None))
            t_type = validate_list_t_type(request.GET.get("t_type", None))
            started_date = validate_start_date(
                request.GET.get("started_at", None))
            end_date = validate_end_date(request.GET.get("end_at", None))
            OFFSET = int(request.GET.get("offset", "0"))
            LIMIT = int(request.GET.get("limit", "10"))

            print(started_date, end_date)
            # 해당계좌의 소유주가 맞는지 확인
            ex_account = check_auth(user_id, account_number)
            if ex_account == None:
                return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)

            filters = self.transaction_list_filter(
                ex_account, started_date, end_date, t_type)

            list_count = Transaction.objects.filter(**filters).count()
            transaction_list = Transaction.objects.filter(
                **filters).order_by("id")[OFFSET:LIMIT]

            results = [{
                '계좌 번호': ex_account.account_number,
                '거래 후 잔액': transaction.balance,
                '금액': transaction.amount,
                '적요': transaction.description,
                '거래 종류': transaction.t_type,
                '거래 일시': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }for transaction in transaction_list]
            return JsonResponse({'Message': 'SUCCESS', 'Data': results, 'TotalCount': list_count}, status=200)
        except AccountAuthError:
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'VALUE ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)

    def transaction_list_filter(self, account, start_date, end_date, t_type):
        filters = {'account': account}

        if t_type == "출금":
            filters['t_type'] = "출금"
        elif t_type == "입금":
            filters['t_type'] = "입금"

        if start_date and end_date:
            filters['created_at__gte'] = start_date
            filters['created_at__lt'] = end_date

        return filters


class SeedView(View):
    def post(self, request):
        try:
            for i in range(1, 11):
                user = User.objects.create(
                    email="test" + str(i) + "@8Percent.com",
                    password=bcrypt.hashpw("1234".encode(
                        'utf-8'), bcrypt.gensalt()).decode('utf-8')
                )
                account = Account.objects.create(
                    user=user,
                    account_number="계좌" + str(i),
                    balance=1000
                )
            account = Account.objects.get(account_number="계좌1")
            for j in range(1, 300000):
                print(j)
                trade(account, 100, "월급", "입금")
                trade(account, 50, "카드값", "출금")
                trade(account, 30, "비트코인", "출금")
                trade(account, 5, "햄버거", "출금")
                trade(account, 5, "피자", "출금")
            return JsonResponse({'Message': 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
