from account.models import Account
from users.models import User


class AccountService:

    # 계좌를 생성하는 함수
    def create_account(self, user: User, account_number: str):
        account = Account.objects.create(
            user=user,
            account_number=account_number,
            balance=0
        )
        return account

    # 계좌를 조회하는 함수
    def select_account(self, account_number: str) -> dict:
        account = Account.objects.filter(account_number=account_number)

        data = {
            "계좌 번호": account[0].account_number,
            "소유주 ": account[0].user.email,
            "잔액": account[0].balance,
        }
        return data
