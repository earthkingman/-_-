import jwt

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from users.models import User
import my_settings
SECRET_KEY = my_settings.SECRET


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'Message': 'INVALID_TOKEN'}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'Message': 'EXPIRED_TOKEN'}, status=403)

        return func(self, request, *args, **kwargs)

    return wrapper


def accessSign(user: User):
    access_token = jwt.encode({'id': user[0].id,
                               "exp": datetime.utcnow() + timedelta(minutes=300)},
                              SECRET_KEY, algorithm="HS256")

    return access_token


# def refreshSign():
#     access_token = jwt.encode({"exp": datetime.utcnow(
#     ) + timedelta(minutes=30000)}, SECRET_KEY, algorithm="HS256")


# def refreshVerify(refresh_token: str, userId: int):
#     try:
#         SECRET_KEY = my_settings.SECRET
#         user = User.objects.get(pk=userId)

#         if refresh_token is user.refresh_token:
#             try:
#                 jwt.decode(access_token, SECRET_KEY, algorithms="HS256")

#             except jwt.exceptions.DecodeError:
#                 raise InvalidAccessTokenError
#             except jwt.ExpiredSignatureError:
#                 raise InvalidAccessTokenError
#         else:
#             raise InvalidAccessTokenError

#     except ValueError:
#         return JsonResponse({'Message': 'ERROR'}, status=400)
#     except KeyError:
#         return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
