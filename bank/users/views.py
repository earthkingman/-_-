import json, re, bcrypt, jwt
from django.http  import JsonResponse
from users.models import User
from django.shortcuts import render

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
