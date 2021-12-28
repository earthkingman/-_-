class Transaction:
    account_number = ""
    amount = 0
    description = ""
    t_type = ""

    def update_account(self, withdraw_amount, ex_account):
        ex_account.balance = ex_account.balance - withdraw_amount
        ex_account.save()
        return ex_account

    def create_transaction(self, withdraw_amount, description, ex_account):
        transaction_history = Transaction.objects.create(
            account = ex_account,
            amount = withdraw_amount,
            balance = ex_account.balance,
            t_type = "출금",
            description = description
        )
        return transaction_history

    def check_exit(authenticated_user, account_number):
            # get_object_or_404() 사용한 방법
            # ex_account = get_object_or_404(Account, account_number = account_number)
            # auth = get_object_or_404(Account, account_number = account_number, user = authenticated_user)
            try:
                ex_account = Account.objects.get(account_number = account_number)
            except Account.DoesNotExist:
                return False
        
    def check_auth(authenticated_user, account_number):
            try:
                ex_account = Account.objects.get(account_number = account_number, user = authenticated_user)
                return ex_account
            except Account.DoesNotExist:
                return False


            
