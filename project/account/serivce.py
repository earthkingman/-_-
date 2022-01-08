from account.models import Account


class AccountService:

    def create_account(self, user, account_number):
        """계좌를 생성하는 함수입니다.

        Args:
            user (User): 사용자
            account_number (str): 계좌 번호
        Return:
            Account (Account): 계좌
        """
        account = Account.objects.create(
            user=user,
            account_number=account_number,
            balance=0
        )
        return account

    def select_account(self, account_number):
        """계좌를 조회하는 함수입니다.

        Args:
            account_number (str): 계좌 번호
        Return:
            data (dict): 계좌 정보
        """
        account = Account.objects.filter(account_number=account_number)

        # 응답 값 생성
        data = {
            "계좌 번호": account[0].account_number,
            "소유주 ": account[0].user.email,
            "잔액": account[0].balance,
        }
        return data
