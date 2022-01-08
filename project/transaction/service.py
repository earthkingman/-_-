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

    # 거래 내역 생성
    def create_transaction(self, amount: int, description: str, account: Account, transaction_type: str):
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

    # 입금 (트랜잭션)
    @transaction.atomic
    def deposit(self, account, amount, description):
        # 계좌 잔액 수정
        account.balance = account.balance + amount
        account.save()
        # 거래 내역 생성
        transaction_history = self.create_transaction(
            amount, description, account, DEPOSIT)

        return transaction_history

    # 출금 (트랜잭션)
    @transaction.atomic
    def withdraw(self, account, amount, description):
        # 계좌 잔액 수정
        account.balance = account.balance - amount
        account.save()
        # 거래 내역 생성
        transaction_history = self.create_transaction(
            amount, description, account, WITHDRAW)  # 거래 내역 생성

        return transaction_history
