from django.test import TestCase, Client
import bcrypt
import jwt
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from users.models import User
from account.models import Account
from importlib import import_module
import my_settings
from django.conf import settings as django_settings
SECRET_KEY = my_settings.SECRET


# class SessionEnabledTestCase(TestCase):

#     def get_session(self):
#         if self.client.session:
#             session = self.client.session
#         else:
#             engine = import_module(django_settings.SESSION_ENGINE)
#             session = engine.SessionStore()
#         return session

#     def set_session_cookies(self, session):
#         # Set the cookie to represent the session
#         session_cookie = django_settings.SESSION_COOKIE_NAME
#         self.client.cookies[session_cookie] = session.session_key
#         cookie_data = {
#             'max-age': None,
#             'path': '/',
#             'domain': django_settings.SESSION_COOKIE_DOMAIN,
#             'expires': None}
#         self.client.cookies[session_cookie].update(cookie_data)


class DealViewTest(TestCase):
    client = Client()

    def setUp(self):

        global headers1, headers2, deal1, deal2, deal3, deal4
        user1 = User.objects.create(email="test1@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        user2 = User.objects.create(email="test2@8Percent.com", password=bcrypt.hashpw(
            "1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

        # # session = self.get_session()
        # session['userId'] = 1
        # session.save()
        # self.set_session_cookies(session)
        # access_token1 = jwt.encode(
        #     {'id': user1.id}, SECRET_KEY, algorithm="HS256")
        # access_token2 = jwt.encode(
        #     {'id': user2.id}, SECRET_KEY, algorithm="HS256")
        # request.session['userId'] = user1.id
        # request.session['userId'] = user2.id
        # session_cookie1 = user1.id
        # session_cookie2 = user2.id
        # headers1 = {'HTTP_Authorization': access_token1}
        # headers2 = {'HTTP_Authorization': access_token2}

        # headers1 = {'Cookie': session}
        # headers2 = {'Cookie': session_cookie2}

        account1 = Account.objects.create(
            user=user1, account_number="계좌1", balance=1000)
        account2 = Account.objects.create(
            user=user2, account_number="계좌2", balance=1000)

        # account1.balance = account1.balance + 1000
        # deal1 = Transaction.objects.create(account = account1, amount = 1000, balance = account1.balance, t_type = "입금", description = "비트코인 매도")

        # account1.balance = account1.balance + 5000
        # deal2 = Transaction.objects.create(account = account2, amount = 5000, balance = account2.balance, t_type = "출금", description = "비트코인 매수")

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        # Transaction.objects.all().delete()

    # 입금 성공
    def test_deal_post_success(self):
        client = Client()

        session = self.client.session
        session['userId'] = [1]
        session.save()
        deal_info = {
            "account_number": "계좌1",
            "amount": 100,
            "description": "월급",
            "t_type": "입금"
        }

        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "Message": "SUCCESS",
            "Data": {
                "거래 계좌": "계좌1",
                "거래 금액": 100,
                "거래 후 금액": 1100,
                "거래 종류": "입금",
                "거래 날짜": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "적요": "월급"
            }})

    # 계좌가 존재하지 않는 경우
    def test_deal_post_account_does_not_exist(self):
        client = Client()

        # session = self.get_session()
        # session['some-key'] = 'some-value'
        # session.save()
        # self.set_session_cookies(session)

        deal_info = {
            "account_number": "존재하지 않는 계좌",
            "amount": 100,
            "description": "월급",
            "t_type": "입금"
        }
        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "EXIST_ERROR"})

    # 출금 잔액이 부족할 경우

    def test_deal_post_insufficient_balance(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": 1000000,
            "description": "월급",
            "t_type": "출금"
        }
        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "BALANCE_ERROR"})

    # 거래 금액이 0보다 같거나 작을 경우
    # def test_deal_post_abnormal_balance(self):
    #     client = Client()

    #     deal_info = {
    #         "account_number":"계좌1",
    #         "amount": -1,
    #         "description": "월급",
    #         "t_type" : "출금"
    #     }
    #     current_time = datetime.now()
    #     response = client.post('/transaction/deposit', json.dumps(deal_info), content_type='application/json', **headers1)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), {"Message": "BALANCE_ERROR"})

    # 계좌 소유주가 아닐 경우
    def test_deal_post_no_permission(self):
        client = Client()

        session = self.client.session
        session["userId"] = 2
        session.save()

        deal_info = {
            "account_number": "계좌2",
            "amount": 10,
            "description": "월급",
            "t_type": "출금"
        }
        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "AUTH_ERROR"})
