import json
import re
import bcrypt
import jwt
from django.views import View
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from users.models import User
from django.shortcuts import render
import my_settings
SECRET_KEY = my_settings.SECRET
# Create your views here.


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            password = str(data['password'])
            hash_password = bcrypt.hashpw(password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'Message': 'USER_ALREADY_EXISTS'}, status=401)
            User.objects.create(
                email=data['email'],
                password=hash_password
            )
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.filter(email=data['email'])
            if not user.exists():
                return JsonResponse({'Message': 'USER_DOES_NOT_EXIST'}, status=401)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                request.session['userId'] = user.id
                # access_token = jwt.encode({'id': user.id, "exp": datetime.utcnow(
                # ) + timedelta(minutes=900000000)}, SECRET_KEY, algorithm="HS256")
                return JsonResponse({'Message': "LOGIN_SUCCESS"}, status=200)

            return JsonResponse({'Message': 'INVALID_PASSWORD'}, status=401)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
