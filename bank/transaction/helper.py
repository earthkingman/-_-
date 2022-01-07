from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction
from transaction.constant import DEPOSIT, WITHDRAW


class AccountAuthError(Exception):
    pass


class TransactionTypeError(Exception):
    pass


class BalanceError(Exception):
    pass


def update_account(amount: int, ex_account: User, t_type: int):
    if (t_type == DEPOSIT):
        ex_account.balance = ex_account.balance + amount
    elif (t_type == WITHDRAW):
        ex_account.balance = ex_account.balance - amount
    else:
        raise TransactionTypeError

    ex_account.save()

    return ex_account


def create_transaction(amount, description, ex_account, t_type):
    if t_type is DEPOSIT:
        t_type = "출금"
    elif t_type is WITHDRAW:
        t_type = "입금"
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

    return ex_account[0]


@transaction.atomic
def trade(ex_account, amount, description, t_type):
    amount_after_transaction = update_account(
        amount, ex_account, t_type)  # 해당 계좌 잔액 수정

    transaction_history = create_transaction(
        abs(amount), description, ex_account, t_type)  # 거래 내역 생성

    if transaction_history.balance is not ex_account.balance:  # 잔액 비교
        raise BalanceConsistencyException

    return transaction_history
