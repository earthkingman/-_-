import json, re, bcrypt, jwt
from django.http  import JsonResponse
from users.models import User
from django.shortcuts import render
import my_settings
SECRET_KEY = my_settings.SECRET
# Create your views here.

def signup(request):
    try:
        print(request.body)
        data = json.loads(request.body)
        print(data)
        hash_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        if User.objects.filter(email=data['email']).exists(): 
            return JsonResponse({'message':'INVALID_EMAIL'},status=400)
        User.objects.create(
                email        = data['email'],
                password     = hash_password
        )
        return JsonResponse({'message':'SUCCESS'},status=201)
    except KeyError:
        return JsonResponse({'message':'ERROR'},status=400)

def login(request):
        try :
            data = json.loads(request.body)
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID_EMAIL'},status=401)

            user = User.objects.get(email= data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm="HS256")

                return JsonResponse({'TOKEN': access_token},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
