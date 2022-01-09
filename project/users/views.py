import json
import re
import bcrypt
import jwt
from django.views import View
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from users.models import User
from django.core.exceptions import ValidationError
from users.service import UserService, UserDuplicateError, PasswordInvalid, UserNotExistError
from users.validators import validate_email, validate_password
import my_settings
SECRET_KEY = my_settings.SECRET


class SignupView(View):
    def post(self, request):
        user_service: UserService = UserService()
        try:
            data = json.loads(request.body)
            email = validate_email(data['email'])
            password = validate_password(data['password'])

            user_service.signup(email, password)

            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)

        except UserDuplicateError:
            return JsonResponse({'Message': 'USER_DUPLICATE'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        user_service: UserService = UserService()
        try:
            data = json.loads(request.body)
            email = validate_email(data['email'])
            password = validate_password(data['password'])

            access_token = user_service.login(email, password)
            return JsonResponse({'ACCESS_TOKEN': access_token}, status=200)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)

        except UserNotExistError:
            return JsonResponse({'Message': 'USER_DOES_NOT_EXIST'}, status=401)

        except PasswordInvalid:
            return JsonResponse({'Message': 'INVALID_PASSWORD'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)

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
