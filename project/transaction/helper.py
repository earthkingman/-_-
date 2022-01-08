from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction
from transaction.constant import DEPOSIT, WITHDRAW


class AccountAuthError(Exception):  # 계좌 권한
    pass


class BalanceError(Exception):  # 잔액 부족
    pass


# 계좌 잔액 수정
def update_account(amount: int, account: User, transaction_type: int):
    if (transaction_type == DEPOSIT):
        account.balance = account.balance + amount
    elif (transaction_type == WITHDRAW):
        account.balance = account.balance - amount

    account.save()

    return account


# 거래 내역 생성
def create_transaction(amount, description, account, transaction_type):
    transaction_history = Transaction.objects.create(
        account=account,
        amount=amount,
        balance=account.balance,
        transaction_type=transaction_type,
        description=description
    )
    return transaction_history


# 권한 확인
def check_auth(user, account_number):
    account = Account.objects.filter(
        account_number=account_number, user=user)

    if not account.exists():
        raise AccountAuthError

    return account[0]


@transaction.atomic  # 거래실행 (트랜잭션)
def trade(account, amount, description, transaction_type):
    amount_after_transaction = update_account(
        amount, account, transaction_type)  # 해당 계좌 잔액 수정

    transaction_history = create_transaction(
        abs(amount), description, account, transaction_type)  # 거래 내역 생성

    return transaction_history
