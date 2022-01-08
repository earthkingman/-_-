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
def update_account(amount: int, account: User, t_type: int):
    if (t_type == DEPOSIT):
        account.balance = account.balance + amount
    elif (t_type == WITHDRAW):
        account.balance = account.balance - amount
    account.save()

    return account


# 거래 내역 생성
def create_transaction(amount, description, account, t_type):
    if t_type is DEPOSIT:
        t_type = "입금"
    elif t_type is WITHDRAW:
        t_type = "출금"
    transaction_history = Transaction.objects.create(
        account=account,
        amount=amount,
        balance=account.balance,
        t_type=t_type,
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

# 거래실행 (트랜잭션)


@transaction.atomic
def trade(account, amount, description, t_type):
    amount_after_transaction = update_account(
        amount, account, t_type)  # 해당 계좌 잔액 수정

    transaction_history = create_transaction(
        abs(amount), description, account, t_type)  # 거래 내역 생성

    if transaction_history.balance is not account.balance:  # 잔액 비교
        raise BalanceConsistencyException

    return transaction_history
