from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction
from transaction.constant import DEPOSIT, WITHDRAW
from datetime import datetime


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
    def deposit(self, account: Account, amount: int, description: str) -> dict:
        # 계좌 잔액 수정
        account.balance = account.balance + amount
        account.save()
        # 거래 내역 생성
        transaction_history: Transaction = self.create_transaction(
            amount, description, account, DEPOSIT)

        data = self.obj_to_data(transaction_history)

        return data

    # 출금 (트랜잭션)
    @transaction.atomic
    def withdraw(self, account: Account, amount: int, description: str) -> tuple:
        # 계좌 잔액 수정
        account.balance = account.balance - amount
        account.save()
        # 거래 내역 생성
        transaction_history: Transaction = self.create_transaction(
            amount, description, account, WITHDRAW)  # 거래 내역 생성

        data = self.obj_to_data(transaction_history)

        return data

    def get_transaction_list(self, account: Account, started_date, end_date, transaction_type: str, offset: int, limit: int) -> list:
        # 필터링
        filters = self.transaction_list_filter(
            account, started_date, end_date, transaction_type)

        # 리스트 갯수
        list_count: int = Transaction.objects.filter(**filters).count()

        # 거래 내역 조회
        transaction_list: Transaction = Transaction.objects.filter(
            **filters).order_by("id")[offset:limit]

        transaction_history: list = self.obj_to_list(transaction_list, account)

        return transaction_history, list_count

        # 데이터 필터링 함수

    def transaction_list_filter(self, account: Account, start_date: str, end_date: str, transaction_type: str) -> dict:
        filters = {'account': account}

        if transaction_type == WITHDRAW:
            filters['transaction_type'] = WITHDRAW
        elif transaction_type == DEPOSIT:
            filters['transaction_type'] = DEPOSIT

        if start_date and end_date:
            filters['created_at__gte'] = start_date
            filters['created_at__lt'] = end_date

        return filters

    def obj_to_data(self, transaction_history: Transaction):
        result = {
            "거래 계좌": transaction_history.account.account_number,
            "거래 금액": transaction_history.amount,
            "거래 후 금액": transaction_history.balance,
            "거래 종류": transaction_history.transaction_type,
            "거래 일시": transaction_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "적요": transaction_history.description
        }
        return result

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
