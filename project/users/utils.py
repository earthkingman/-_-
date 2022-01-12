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

        except User.DoesNotExist:
            return JsonResponse({'Message': 'INVALID_USER'}, status=403)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'Message': 'INVALID_TOKEN'}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'Message': 'EXPIRED_TOKEN'}, status=403)

        return func(self, request, *args, **kwargs)

    return wrapper


def accessSign(user: User):
    access_token = jwt.encode({'id': user[0].id
                               # "exp": datetime.utcnow() + timedelta(minutes=300)
                               },
                              SECRET_KEY, algorithm="HS256")

    return access_token
