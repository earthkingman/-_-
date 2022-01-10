from account.models import Account
from users.models import User


class ExitsError(Exception):  # 계좌 존재 X
    pass


class AccountAuthError(Exception):  # 계좌 권한
    pass


class AccountDuplicateError(Exception):  # 계좌 중복
    pass


class AccountService:

    # 계좌를 생성하는 함수
    def create_account(self, user: User, account_number: str):

        if Account.objects.filter(account_number=account_number).exists():
            raise AccountDuplicateError

        account = Account.objects.create(
            user=user,
            account_number=account_number,
            balance=0
        )
        return account

    # 계좌를 조회하는 함수
    def select_account(self, user, account_number):
        if not Account.objects.filter(account_number=account_number).exists():
            raise ExitsError

        account = Account.objects.filter(
            account_number=account_number, user=user)

        if not account.exists():
            raise AccountAuthError

        data = {
            "계좌 번호": account[0].account_number,
            "소유주 ": account[0].user.email,
            "잔액": account[0].balance,
        }
        return data
