from django.test import TestCase, Client
import bcrypt
import jwt
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from users.models import User
from account.models import Account
from importlib import import_module
from transaction.service import TransactionService
from transaction.constant import WITHDRAW, DEPOSIT
import my_settings
from django.conf import settings as django_settings
SECRET_KEY = my_settings.SECRET


class AccountViewTest(TestCase):
    client = Client()

    def setUp(self):
        trasaction_service: TransactionService = TransactionService()
        global headers1, headers2, deal1, deal2, deal3, deal4
        user1 = User.objects.create(email="test1@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        user2 = User.objects.create(email="test2@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

        access_token1 = jwt.encode(
            {'id': user1.id}, SECRET_KEY, algorithm="HS256")
        access_token2 = jwt.encode(
            {'id': user2.id}, SECRET_KEY, algorithm="HS256")

        headers1 = {'HTTP_Authorization': access_token1}
        headers2 = {'HTTP_Authorization': access_token2}

        account1 = Account.objects.create(
            user=user1, account_number="계좌1", balance=1000)
        account2 = Account.objects.create(
            user=user2, account_number="계좌2", balance=1000)

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        # Transaction.objects.all().delete()

    # 계좌 생성
    def test_account_post_success(self):
        client = Client()

        deal_info = {
            "account_number": "계좌3",
            "amount": 100
        }

        response = client.post('/accounts/account', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Message": "SUCCESS"})

    # 계좌 중복

    def test_account_post_duplicate(self):
        client = Client()

        deal_info = {
            "account_number": "계좌2",
            "amount": 100
        }

        response = client.post('/accounts/account', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "DUPLICATE_ERROR"})

      # 계좌 조회
    def test_account_get_success(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌2', **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            "Data": {'계좌 번호': '계좌2', '소유주 ': 'test2@8Percent.com', '잔액': 1000}
        })
