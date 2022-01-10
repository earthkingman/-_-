import json
from django.views import View
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from users.service import UserService
from users.error import UserDuplicateError, PasswordInvalidError, UserNotExistError
from users.validators import validate_email, validate_password
import my_settings
SECRET_KEY = my_settings.SECRET


class SignupView(View):
    def post(self, request):
        user_service: UserService = UserService()
        try:
            data = json.loads(request.body)
            email: str = validate_email(data['email'])
            password: str = validate_password(data['password'])

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
            email: str = validate_email(data['email'])
            password: str = validate_password(data['password'])

            access_token = user_service.login(email, password)
            return JsonResponse({'ACCESS_TOKEN': access_token}, status=200)

        except ValidationError as detail:
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)

        except UserNotExistError:
            return JsonResponse({'Message': 'EMAIL_DOES_NOT_EXIST'}, status=401)

        except PasswordInvalidError:
            return JsonResponse({'Message': 'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'Message': 'JSON_DECODE_ERROR'}, status=400)
