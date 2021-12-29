from django.test import TestCase, Client
import bcrypt
from unittest.mock import MagicMock, patch
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
      
    def test_signupview_post_duplicated_user(self):
        client = Client()
        user = {
            "email": "ji-park@42seoul.com",
            "password": "42seoul",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "USER_ALREADY_EXISTS"})

class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="ji-park@42seoul.com",
            password=bcrypt.hashpw('42seoul'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )
    def tearDown(self):
        User.objects.all().delete()

    def test_login_success(self):
        client = Client()
        user = {
            "email" : "ji-park@42seoul.com",
            "password" : "42seoul",
        }

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_login_unregistered_user(self):
        client = Client()
        user = {
            "email" : "ji-park2@42seoul.com",
            "password" : "42seoul",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "USER_DOES_NOT_EXIST"})


    def test_login_invalid_password(self):
        client = Client()
        user = {
            "email" : "ji-park@42seoul.com",
            "password" : "42seoul2",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "INVALID_PASSWORD"})