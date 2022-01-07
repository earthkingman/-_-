from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction


class AccountAuthError(Exception):
    pass


class TransactionTypeError(Exception):
    pass


class BalanceError(Exception):
    pass


def update_account(amount, ex_account, t_type):
    if (t_type == "입금"):
        ex_account.balance = ex_account.balance + amount
    elif (t_type == "출금"):
        ex_account.balance = ex_account.balance - amount
    else:
        raise TransactionTypeError
    ex_account.save()
    return ex_account


def create_transaction(amount, description, ex_account, t_type):
    transaction_history = Transaction.objects.create(
        account=ex_account,
        amount=amount,
        balance=ex_account.balance,
        t_type=t_type,
        description=description
    )
    return transaction_history


def check_auth(user_id, account_number):
    ex_account = Account.objects.filter(
        account_number=account_number, user_id=user_id)
    if not ex_account.exists():
        raise AccountAuthError
    return ex_account


@transaction.atomic
def trade(ex_account, amount, description, t_type):

    amount_after_transaction = update_account(
        amount, ex_account, t_type)  # 해당 계좌 잔액 수정

    transaction_history = create_transaction(
        abs(amount), description, ex_account, t_type)  # 거래 내역 생성

    if transaction_history.balance is not ex_account.balance:  # 잔액 비교
        raise BalanceConsistencyException
    data = {
        "거래 계좌": transaction_history.account.account_number,
        "거래 금액": transaction_history.amount,
        "거래 후 금액": transaction_history.balance,
        "거래 종류": transaction_history.t_type,
        "거래 날짜": transaction_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "적요": description
    }
    return data
