from django.test import TestCase, Client
import bcrypt
from datetime import datetime
import json
from users.models import User
# Create your tests here.


class SignUpTest(TestCase):
    def test_signup_success(self):
        client = Client()
        user = {
            "email": "Mark1@stark.com",
            "password": "mark486**",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Message": "SUCCESS"})

    def setUp(self):
        User.objects.create(
            email="ji-park@42seoul.com",
            password="42seoul",
        )

    def tearDown(self):
        User.objects.all().delete()

    # 회원가입 아이디 중복
    def test_signupview_post_duplicated_user(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "42seoul",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "USER_DUPLICATE"})


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="ji-park@42seoul.com",
            password=bcrypt.hashpw('42seoul'.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )

    def tearDown(self):
        User.objects.all().delete()

    # 로그인 성공
    def test_login_post_success(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "42seoul",
        }

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    # 회원가입 JSON_ERROR
    def test_signup_json_error_post_fail(self):
        client = Client()

        current_time = datetime.now()

        user = {
            current_time,
        }

        response = client.post(
            "/users/signup", user, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "JSON_DECODE_ERROR"})

    # 로그인 JSON_ERROR
    def test_login_json_error_post_fail(self):
        client = Client()

        current_time = datetime.now()

        user = {
            current_time,
        }

        response = client.post(
            "/users/login", user, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "JSON_DECODE_ERROR"})

    # 회원가입 비밀번호 VALIDATION_ERROR
    def test_signup_validatation_password_error_post_fail(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "",
        }

        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         "Message": "VALIDATION_ERROR['비밀번호 길이는 3보다 크고 20보다 작아야 합니다']"})

    # 로그인 비밀번호 VALIDATION_ERROR

    def test_login_validatation_password_error_post_fail(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "",
        }

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         "Message": "VALIDATION_ERROR['비밀번호 길이는 3보다 크고 20보다 작아야 합니다']"})

  # 로그인 이메일 VALIDATION_ERROR
    def test_login_validatation_email_error_post_success(self):
        client = Client()
        user = {
            "email": "ji-park11111111111111111111111111111111111111111111111111111111@42seoul.com1111111111111111311",
            "password": "42seoul",
        }

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         "Message": "VALIDATION_ERROR['이메일 길이는 3보다 크고 20보다 작아야 합니다']"})

    # 미등록 아이디
    def test_login_unregistered_user_post_fail(self):
        client = Client()
        user = {
            "email": "ji-park2@42seoul.com",
            "password": "42seoul",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "EMAIL_DOES_NOT_EXIST"})

    # 비밀번호 오류
    def test_login_invalid_password_post_fail(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "42seoul2",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "INVALID_PASSWORD"})
