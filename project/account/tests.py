from django.test import TestCase, Client
import bcrypt
import jwt
import json
from datetime import datetime, timedelta
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
        global headers1, headers2, headers3, headers4, deal1, deal2, deal3, deal4
        user1 = User.objects.create(email="test1@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        user2 = User.objects.create(email="test2@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

        access_token1 = jwt.encode(
            {'id': user1.id}, SECRET_KEY, algorithm="HS256")
        access_token2 = jwt.encode(
            {'id': user2.id}, SECRET_KEY, algorithm="HS256")
        access_token3 = jwt.encode(
            {'id': 10}, "dwwqewqeqweqwee", algorithm="HS256")
        # access_token3 = jwt.encode(
        #     {'id': user1.id, "exp": datetime.utcnow() + timedelta(seconds=0)}, SECRET_KEY, algorithm="HS256")
        access_token4 = jwt.encode(
            {'id': 10}, SECRET_KEY, algorithm="HS256")

        headers1 = {'HTTP_Authorization': access_token1}
        headers2 = {'HTTP_Authorization': access_token2}
        headers3 = {'HTTP_Authorization': access_token3}
        headers4 = {'HTTP_Authorization': access_token4}

        account1 = Account.objects.create(
            user=user1, account_number="계좌1", balance=1000)
        account2 = Account.objects.create(
            user=user2, account_number="계좌2", balance=1000)

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        # Transaction.objects.all().delete()

    # 계좌 생성 성공
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

    # 계좌 생성 KEY_ERROR
    def test_account_key_error_post_fail(self):
        client = Client()

        deal_info = {
            "amount": 100
        }

        response = client.post('/accounts/account', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'Message': "KEY_ERROR", })

    # 계좌 생성 JSON_DECODE_ERROR

    def test_account_json_error_post_fail(self):
        client = Client()

        current_time = datetime.now()
        deal_info = current_time

        response = client.post('/accounts/account', deal_info,
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'Message': "JSON_DECODE_ERROR", })

    # 계좌 생성 중복
    def test_account_duplicate_post_fail(self):
        client = Client()

        deal_info = {
            "account_number": "계좌2",
            "amount": 100
        }

        response = client.post('/accounts/account', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "DUPLICATE_ERROR"})

       # 계좌 생성 거래 금액VALIDATION_ERROR
    def test_account_validation_post_fail(self):
        client = Client()

        deal_info = {
            "account_number": "계좌2",
            "amount": '100원'
        }

        response = client.post('/accounts/account', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['정수를 넣어주세요']"
        })

      # 계좌 정보 조회 권한 없음
    def test_account_auth_get_fail(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌2', **headers1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'Message': 'AUTH_ERROR'
        })

    # 계좌 정보 조회 성공
    def test_account_get_success(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌1', **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            "Data": {'계좌 번호': '계좌1', '소유주 ': 'test1@8Percent.com', '잔액': 1000}
        })

        # 계좌 정보 조회 EXIST_ERROR
    def test_account_exist_error_get_fail(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌1234', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': 'EXIST_ERROR'
        })

    # 계좌 정보 조회 VALIDATION_ERROR
    def test_account_validation_error_get_fail(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌1234556456456464564564564646465645645646', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['계좌번호 길이는 2보다 크고 20보다 작아야 합니다']"
        })

    # # 계좌 정보 조회 토큰은 있지만 토큰 정보에 유저가 없는 경우 실패
    # def test_account_auth_user_get_fail(self):
    #     client = Client()

    #     response = client.get(
    #         '/accounts/account?account_number=계좌1', **headers4)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), {
    #         'Message': 'INVALID_USER'
    #     })
    # 계좌 정보 조회 토큰 없는 경우 실패

    def test_account_no_auth_get_fail(self):
        client = Client()

        response = client.get(
            '/accounts/account?account_number=계좌1')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'Message': 'INVALID_TOKEN'
        })

    # 계좌 정보 조회 토큰 만료

    # def test_account_expired_get_fail(self):
    #     client = Client()

    #     response = client.get(
    #         '/accounts/account?account_number=계좌1', **headers3)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), {
    #         'Message': 'EXPIRED_TOKEN'
    #     })
