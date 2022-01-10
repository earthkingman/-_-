from django.test import TestCase, Client
import bcrypt
import jwt
import json
from datetime import datetime
from users.models import User
from account.models import Account
from importlib import import_module
from transaction.service import TransactionService
from .constant import WITHDRAW, DEPOSIT
import my_settings
from django.conf import settings as django_settings
SECRET_KEY = my_settings.SECRET


class TransactionViewTest(TestCase):
    client = Client()

    def setUp(self):
        trasaction_service: TransactionService = TransactionService()
        global headers1, headers2, deal1, deal2, deal3, deal4, account1
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

        deal1 = trasaction_service.deposit("계좌1", 100, "비트코인 매도")
        deal2 = trasaction_service.withdraw("계좌1", 100, "비트코인 매수")
        deal3 = trasaction_service.deposit("계좌1", 100, "비트코인 매도")
        deal4 = trasaction_service.withdraw("계좌1", 100, "비트코인 매수")

        # account1.balance = account1.balance + 1000
        # deal1 = Transaction.objects.create(account = account1, amount = 1000, balance = account1.balance, transaction_type = "입금", description = "비트코인 매도")

        # account1.balance = account1.balance + 5000
        # deal2 = Transaction.objects.create(account = account2, amount = 5000, balance = account2.balance, transaction_type = "출금", description = "비트코인 매수")

    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        # Transaction.objects.all().delete()

    # 입금 성공
    def test_deposit_post_success(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": 100,
            "description": "월급",
        }

        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "Message": "SUCCESS",
            "Data": {
                "거래 계좌": "계좌1",
                "거래 금액": 100,
                "거래 후 금액": 1100,
                "거래 종류": "입금",
                "거래 일시": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "적요": "월급"
            }})

    # 출금 성공
    def test_withdraw_post_success(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": 100,
            "description": "비트코인 매수",
        }

        current_time = datetime.now()
        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "Message": "SUCCESS",
            "Data": {
                "거래 계좌": "계좌1",
                "거래 금액": 100,
                "거래 후 금액": 900,
                "거래 종류": "출금",
                "거래 일시": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "적요": "비트코인 매수"
            }})

    # 출금 금액 검증 에러
    def test_withdraw_validate_amount_post_fail(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": "100원",
            "description": "비트코인 매수",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['정수를 넣어주세요']", })

    # 입금 적요 길이 검증 에러
    def test_withdraw_validate_description_post_fail(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": "100",
            "description": "",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['적요 길이는 0보다 크고 20보다 작아야 합니다']", })

    # 출금 계좌 번호 길이 검증 에러
    def test_withdraw_validate_account_post_fail(self):
        client = Client()

        deal_info = {
            "account_number": "_",
            "amount": "100",
            "description": "비트코인 매수",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['계좌번호 길이는 2보다 크고 20보다 작아야 합니다']", })

    # 입금 JSON_DECODE_ERROR
    def test_deposit_json_post_fail(self):
        client = Client()

        current_time = datetime.now()
        deal_info = {
            current_time,
        }
        current_time = datetime.now()
        response = client.post('/transaction/deposit', deal_info,
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "JSON_DECODE_ERROR", })

    # 출금 JSON_DECODE_ERROR
    def test_withdraw_json_post_fail(self):
        client = Client()
        current_time = datetime.now()
        deal_info = {
            current_time,
        }
        current_time = datetime.now()
        response = client.post('/transaction/withdraw', deal_info,
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "JSON_DECODE_ERROR", })

    # 출금 KEY_ERROR
    def test_withdraw_validate_key_post_fail(self):
        client = Client()

        deal_info = {

            "description": "비트코인 매수",
        }

        current_time = datetime.now()
        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'Message': "KEY_ERROR", })

    # 입금 KEY_ERROR
    def test_deposit_validate_post_success(self):
        client = Client()

        deal_info = {

            "description": "비트코인 매수",
        }

        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "KEY_ERROR", })

    # 계좌가 존재하지 않는 경우
    def test_deposit_post_account_does_not_exist(self):
        client = Client()

        deal_info = {
            "account_number": "존재하지 않는 계좌",
            "amount": 100,
            "description": "월급",
        }

        current_time = datetime.now()
        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "EXIST_ERROR"})

    # 출금 잔액이 부족할 경우
    def test_withdraw_post_insufficient_balance(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": 1000000,
            "description": "월급",
        }

        current_time = datetime.now()
        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "BALANCE_ERROR"})

    # 출금 거래 금액이 0보다 같거나 작을 경우
    def test_withdraw_post_abnormal_balance(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": -1,
            "description": "월급",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'Message': "VALIDATION_ERROR['0보다 같거나 작은 금액은 거래할 수 없습니다.']"})

    # 입금 거래 금액이 0보다 같거나 작을 경우
    def test_deposit_post_abnormal_balance(self):
        client = Client()

        deal_info = {
            "account_number": "계좌1",
            "amount": -1,
            "description": "월급",
        }

        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'Message': "VALIDATION_ERROR['0보다 같거나 작은 금액은 거래할 수 없습니다.']"})

    # 입금 계좌 소유주가 아닐 경우
    def test_deposit_post_no_permission(self):
        client = Client()

        deal_info = {
            "account_number": "계좌2",
            "amount": 10,
            "description": "월급",
        }

        response = client.post('/transaction/deposit', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "AUTH_ERROR"})

    # 출금 계좌 소유주가 아닐 경우
    def test_withdraw_post_no_permission(self):
        client = Client()

        deal_info = {
            "account_number": "계좌2",
            "amount": 10,
            "description": "월급",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "AUTH_ERROR"})

    # 출금 계좌 존재 확인
    def test_withdraw_post_exist_account(self):
        client = Client()

        deal_info = {
            "account_number": "계좌4",
            "amount": 10,
            "description": "월급",
        }

        response = client.post('/transaction/withdraw', json.dumps(deal_info),
                               content_type='application/json', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "EXIST_ERROR"})

    #  계좌 리스트 조회
    def test_transaction_list_get_success(self):
        client = Client()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2', **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            'Data': [
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1100, '금액': 100, '적요': '비트코인 매도',
                    '거래 종류': '입금', '거래 일시': deal1['거래 일시']
                },
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1000, '금액': 100, '적요': '비트코인 매수',
                    '거래 종류': '출금', '거래 일시': deal2['거래 일시']
                }
            ],
            "TotalCount": 4
        })

    # 거래 내역 조회 날짜로 조회하는 경우
    def test_transaction_list_started_at_end_at_success(self):
        client = Client()
        current_time = datetime.now()
        start_date: datetime = current_time.strftime("%Y-%m-%d")
        end_date: datetime = current_time.strftime("%Y-%m-%d")
        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&started_at=' + start_date + '&end_at=' + end_date, **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            'Data': [
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1100, '금액': 100, '적요': '비트코인 매도',
                    '거래 종류': '입금', '거래 일시': deal1['거래 일시']
                },
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1000, '금액': 100, '적요': '비트코인 매수',
                    '거래 종류': '출금', '거래 일시': deal2['거래 일시']
                }
            ],
            "TotalCount": 4
        })

    # 거래 내역  입금으로 조회
    def test_transaction_list_transaction_type_deposit_success(self):
        client = Client()
        current_time = datetime.now()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&transaction_type=입금', **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            'Data': [
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1100, '금액': 100, '적요': '비트코인 매도',
                    '거래 종류': '입금', '거래 일시': deal1['거래 일시']
                },
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1100, '금액': 100, '적요': '비트코인 매도',
                    '거래 종류': '입금', '거래 일시': deal3['거래 일시']
                }
            ],
            "TotalCount": 2
        })

        # 거래 내역  출금으로 조회
    def test_transaction_list_transaction_type_withdraw_success(self):
        client = Client()
        current_time = datetime.now()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&transaction_type=출금', **headers1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'Message': 'SUCCESS',
            'Data': [
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1000, '금액': 100, '적요': '비트코인 매수',
                    '거래 종류': '출금', '거래 일시': deal2['거래 일시']
                },
                {
                    '계좌 번호': '계좌1', '거래 후 잔액': 1000, '금액': 100, '적요': '비트코인 매수',
                    '거래 종류': '출금', '거래 일시': deal4['거래 일시']
                }
            ],
            "TotalCount": 2
        })

        # 거래 내역 조회 출입금 예외
    def test_transaction_list_transaction_type_withdraw_fail(self):
        client = Client()
        current_time = datetime.now()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&transaction_type=출ㅇㅇㅇ금', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': "VALIDATION_ERROR['거래는 출금과 입금, 기본만 가능합니다.']"
        })

   # 거래 내역 조회 시작 날짜가 잘못된 경우
    def test_transaction_list_started_at_end_at_fail(self):
        client = Client()
        current_time = datetime.now()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&started_at=2023332-01-06&end_at=2022-01333-08', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'Message': "VALIDATION_ERROR['날짜 형식이 아닙니다.']"
                         })

  # 거래 내역 조회 종료 날짜가 잘못된 경우
    def test_transaction_list_end_at_end_at_fail(self):
        client = Client()
        current_time = datetime.now()

        response = client.get(
            '/transaction/list?account_number=계좌1&offset=0&limit=2&started_at=2022-01-06&end_at=2022-01333-08', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         'Message': "VALIDATION_ERROR['날짜 형식이 아닙니다.']"
                         })

    # 거래 내역 조회 계좌가 존재하지 않는 경우
    def test_transaction_list_get_not_exist(self):
        client = Client()

        response = client.get(
            '/transaction/list?account_number=계좌번호1004&offset=0&limit=10', **headers1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'Message': 'EXIST_ERROR'
        })

    # 거래 내역 조회 계좌 권한이 없는 경우
    def test_transaction_get_list_no_permission(self):
        client = Client()

        response = client.get(
            '/transaction/list?account_number=계좌2&offset=0&limit=10', **headers1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'Message': 'AUTH_ERROR'
        })

    #   # 거래 내역 조회
    # def test_transaction_get_list_no_permission(self):
    #     client = Client()

    #     response = client.get(
    #         '/transaction/list?account_number=계좌2&offset=0&limit=10', **headers1)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), {
    #         'Message': 'AUTH_ERROR'
    #     })
