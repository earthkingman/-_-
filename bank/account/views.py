import json
from django.views          import View
from django.shortcuts import render
from django.http  import JsonResponse

from django.db.models      import Q # Where절에 Or 문을 추가하고 싶다면 사용
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger

from users.utils    import login_decorator
from account.models import Account
from transaction.models import Transaction
from users.models import User


# Create your views here.

class AccountView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            # if data['account'] == null or data['balance']:
            #     return JsonResponse({'Message':'ERROR'},status=400)
            # user = User.objects.get(id=userId)
            Account.objects.create(
                user = user,
                account_number = data['account'],
                balance = data['balance']
            )
            return JsonResponse({'Message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400)
    
    @login_decorator ## 해당 계좌, 페이지
    def get(self, request):
        try:
            user = request.user
            account_number = request.GET.get("account_number", None)
            page = request.GET.get('page',1)

             ## 해당계좌의 소유주가 맞는지 확인
            ex_account = Account.objects.get(account_number = account_number, user_id = user.id)
            if ex_account == None :
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)

            transaction_list = Transaction.objects.filter(account_id = ex_account.id)
            paginator = Paginator(transaction_list, 100)
            page_obj = paginator.page(3)

            results = [{
            '계좌 번호'   : ex_account.account_number,
            '거래 후 잔액': page.balance,
            '금액'      : page.amount,
            '적요'      : page.description,
            '거래 종류'  : page.t_type,
            '거래 일시'  : page.created_at
            }for page in page_obj]
            
            return JsonResponse({'Message':'SUCCESS', 'Data': results}, status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'}, status=400)

       