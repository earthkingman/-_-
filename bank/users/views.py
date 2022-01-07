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
from users.utils import accessSign, accessVerify
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
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'Message': 'USER_DOES_NOT_EXIST'}, status=401)

            user = User.objects.filter(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):  # 원리 파악하기
                access_token = accessSign(user)
                return JsonResponse({'ACCESS_TOKEN': access_token}, status=200)

            return JsonResponse({'Message': 'INVALID_PASSWORD'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)


# class RefreshView(View):
#     def post(self, request):
#         try:
#             access_token = request.headers.get('Authorization', None)
#             refresh_token = request.headers.get('Refresh', None)

#             if (access_token and refresh_token):  # access_token refresh_token 둘 다 존재하는 경우
#                 auth_result = accessVerify(access_token)
#                 except:
#             if
#             else:
#                 return JsonResponse({'Message': 'ACCESS_TOKEN_AND_REFRESH_TOKEN_EXPIRED'}, status=400)

#         except InvalidAccessTokenError:
#             return JsonResponse({'Message': 'INVALID_TOKEN_ERROR'}, status=400)
#         except JSONDecodeError:
#             return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)
#         except ValueError:
#             return JsonResponse({'Message': 'ERROR'}, status=400)
#         except KeyError:
#             return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
