from transaction.models import Transaction
from users.models import User
from account.models import Account
from django.db import transaction

class Trade:
    
    def update_account(self, amount, ex_account):
        ex_account.balance = ex_account.balance + amount
        if ex_account.balance < 0:
            return False
        ex_account.save()
        return ex_account

    def create_transaction(self, amount, description, ex_account, t_type):
        transaction_history = Transaction.objects.create(
            account = ex_account,
            amount = amount,
            balance = ex_account.balance,
            t_type = t_type,
            description = description
        )
        return transaction_history

    def check_exit(self, authenticated_user, account_number):
            # get_object_or_404() 사용한 방법
            # ex_account = get_object_or_404(Account, account_number = account_number)  -> 명확한 에러를 못보여줌
            # auth = get_object_or_404(Account, account_number = account_number, user = authenticated_user)
            try: # 명확한 에러를 보여줌
                ex_account = Account.objects.get(account_number = account_number)
            except Account.DoesNotExist:
                return False

    def check_auth(self, authenticated_user, account_number):
            try:
                ex_account = Account.objects.get(account_number = account_number, user = authenticated_user)
                return ex_account
            except Account.DoesNotExist:
                return False
    
    @transaction.atomic
    def trade(self, ex_account, amount, description, t_type):
        
        if t_type == "출금":
            amount_after_transaction = self.update_account(amount * -1, ex_account) #해당 계좌 잔액 수정
        elif t_type == "입금":
            amount_after_transaction = self.update_account(amount, ex_account) #해당 계좌 잔액 수정
        
        if amount_after_transaction == False : # 잔액 부족으로 거래 불가능
            return False
        transaction_history = self.create_transaction(amount, description, ex_account, t_type) #거래 내역 생성
        
        data = {
            "거래 계좌" : transaction_history.account.account_number,
            "거래 금액" : transaction_history.amount,
            "거래 후 금액" : transaction_history.balance,
            "거래 종류" : transaction_history.t_type,
            "거래 날짜" : transaction_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "적요" : description
        }
        return data