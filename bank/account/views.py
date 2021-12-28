import json
from django.views          import View
from django.shortcuts import render
from django.http  import JsonResponse
from users.utils    import login_decorator
from account.models import Account
from users.models import User
# Create your views here.

class AccountView(View):
    @login_decorator
    def post(self, request):
            try:
                data = json.loads(request.body)
                userId = request.user
                # if data['account'] == null or data['balance']:
                #     return JsonResponse({'Message':'ERROR'},status=400)
                # user = User.objects.get(id=userId)
                print(userId, data['account'], data['balance'])
                Account.objects.create(
                    user = userId,
                    account_number = data['account'],
                    balance = data['balance']
                )
                return JsonResponse({'Message':'SUCCESS'},status=201)

            except KeyError:
                return JsonResponse({'Message':'ERROR'},status=400)