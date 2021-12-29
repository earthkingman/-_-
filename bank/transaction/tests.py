from django.test import TestCase, Client
import bcrypt, jwt, json
from unittest.mock import MagicMock, patch

from users.models import User
from account.models import Account

import my_settings
SECRET_KEY = my_settings.SECRET

class DealViewTest(TestCase) :
    def setUp(self) :
        global headers1, headers2, deal1, deal2, deal3, deal4
        
        user1 = User.objects.create(email = "test1@8Percent.com",password = bcrypt.hashpw("1234".encode('utf-8'),bcrypt.gensalt()).decode('utf-8'))
        user2 = User.objects.create(email = "test2@8Percent.com",password=bcrypt.hashpw("1234".encode('utf-8'),bcrypt.gensalt()).decode('utf-8'))

    

        access_token1  = jwt.encode({'id':user1.id}, SECRET_KEY, algorithm="HS256")
        access_token2  = jwt.encode({'id':user2.id}, SECRET_KEY, algorithm="HS256")
        

        headers1       = {'Authorization' : access_token1}
        headers2       = {'Authorization' : access_token2}
        

        account1 = Account.objects.create(user = user1, account_number = "계좌1", balance = 1000)
        account2 = Account.objects.create(user = user2, account_number = "계좌2", balance = 1000)

        # account1.balance = account1.balance + 1000
        # deal1 = Transaction.objects.create(account = account1, amount = 1000, balance = account1.balance, t_type = "입금", description = "비트코인 매도")

        # account1.balance = account1.balance + 5000
        # deal2 = Transaction.objects.create(account = account2, amount = 5000, balance = account2.balance, t_type = "출금", description = "비트코인 매수")
    

    def tearDown(self) :
        User.objects.all().delete()
        Account.objects.all().delete()
        # Transaction.objects.all().delete()
    
    ## 거래 성공
    def test_deal_post_success(self):
        client = Client()
        
        deal_info = {
        "account_number":"계좌1",
        "amount":100,
        "description": "월급",
        "t_type" : "입금"
        }
        
        response = client.post('/transaction/deposit', json.dumps(deal_info), content_type='application/json', **headers1)
        print(response)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json(),{
        # "Message": "SUCCESS",
        # "Data": {
        # "거래 계좌": "계좌1",
        # "거래 금액": 100,
        # "거래 후 금액": 2735,
        # "거래 종류": "입금",
        # "거래 날짜": "2021-12-29 14:56:04",
        # "적요": "월급"
        # }})

    ## 계좌가 존재하지 않는 경우