from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction
from transaction.constant import DEPOSIT, WITHDRAW


class ExitsError(Exception):  # 계좌 존재 X
    pass


class AccountAuthError(Exception):  # 계좌 권한
    pass


class BalanceError(Exception):  # 잔액 부족
    pass


class TransactionService:
    # 계좌 잔액 수정
    def update_account(self, amount: int, account: User, transaction_type: int):
        if (transaction_type == DEPOSIT):
            account.balance = account.balance + amount
        elif (transaction_type == WITHDRAW):
            account.balance = account.balance - amount

        account.save()

        return account

    # 거래 내역 생성
    def create_transaction(self, amount, description, account, transaction_type):
        transaction_history = Transaction.objects.create(
            account=account,
            amount=amount,
            balance=account.balance,
            transaction_type=transaction_type,
            description=description
        )
        return transaction_history

    # 계좌 존재 및 권한 확인
    def check_auth(self, user, account_number):
        if not Account.objects.filter(account_number=account_number).exists():
            raise ExitsError

        account = Account.objects.filter(
            account_number=account_number, user=user)

        if not account.exists():
            raise AccountAuthError

        return account[0]

    # 거래실행 (트랜잭션)
    @transaction.atomic
    def trade(self, account, amount, description, transaction_type):
        amount_after_transaction = self.update_account(
            amount, account, transaction_type)  # 해당 계좌 잔액 수정

        transaction_history = self.create_transaction(
            abs(amount), description, account, transaction_type)  # 거래 내역 생성

        return transaction_history
