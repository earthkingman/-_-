# 8퍼센트

### 1. 과제 안내

1. REST API 기능

   - 거래내역 조회 API
   - 입금 API
   - 출금 API

2. 개발 조건
   - 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
   - DB를 설계 할때 각 칼럼의 타입과 제약

3. 빌드 및 실행 방법

### 2. 사전 과제에 임하는 나의 로드맵 

<img src = "https://user-images.githubusercontent.com/48669085/148150277-694354fa-5d91-473b-a8fc-156f83cd8f48.png" width="800px">

### 3. 사전과제가 요구한 것

<img src = "https://user-images.githubusercontent.com/48669085/148150818-fd921844-42cc-428c-a2fc-c2d644cc55f2.png" width="700px">

### 4. 일정 관리

<img src = "https://user-images.githubusercontent.com/48669085/148113051-5bccce86-47b4-42f1-bf18-1a15289805c1.png" width="500px">

### 5. 개발 환경 및 프로젝트 구조

<img src = "https://user-images.githubusercontent.com/48669085/148112357-ccc98696-53e8-46b1-83f9-089fddf7b456.png" width="650px">
    

    - python 3.9.1
    - django 4.0
    - sqlite

### 6. 데이터베이스 관계

- DB를설계할때각칼럼의타입과제약
  ![image](https://user-images.githubusercontent.com/48669085/148112594-04cf1932-7ab7-455f-84d8-9a28773ecd95.png)

### 6. 디렉토리 구조

```bash
├── Makefile
├── README.md
├── bank
│   ├── account
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── migrations
│   │ 
│   ├── transaction
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │  
│   ├── urls.py
│   │ 
│   ├── users
│   │   ├── admin.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests
│   │   ├── urls.py
│   │   └── views.py
│   └── wsgi.py
│
└── manage.py

```

### 7. API 명세

### 8. API 설명

#### 계좌 생성 API

로그인을 한 사용자만 계좌를 생성할 수 있습니다.

그래서 사용자를 검증하는 로직이 필요했고, 데코레이터 함수를 사용해서 구현했습니다. 

그리고 데코레이터 함수를 사용해서 계좌를 생성하는 함수를 변경하지 않고 사용자를 검증하는 로직을 추가할 수 있었습니다.

  ```python
  def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            SECRET_KEY = my_settings.SECRET
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper

  ```

  계좌는 로그인을 한 유저만 생성할 수 있어야하고 계좌는 사용자와 연결되어 있어야 한다고 생각했습니다. 

  그래서 계좌를 생성할 때 request객체 안에있는 user를 가지고 온 다음 계좌를 생성했습니다.

  그리고 계좌명은 중복이 되면 안된다고 생각했습니다. 테이블에서  계좌명을 Unique 키로 사용하고 있지만, 

  계좌가 중복이 되는 경우에 명확한 에러가 사용자에게 보여지지 않았습니다.  그래서 계좌가 중복되는 경우엔 따로 예외처리를 적용했습니다.

```python
class AccountView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            if Account.objects.filter(account_number=data['account']).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)

            Account.objects.create(
                user=user,
                account_number=data['account'],
                balance=data['balance']
            )
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
```

#### 출금 및 입금 API

사용자가 가지고 있는 자기의 계좌만 출금과 입금이 가능합니다. 저는 출금과 입금의 공통점은 거래라고 생각했습니다.

TradeClass 만들고 Deposit View와 Withdraw View가 상속하도록 구현했습니다. 

그리고 TradeClass에 잔액 수정, 권한을 확인, 거래내역 생성, 잔액 예외처리, 거래가 진행되는 메소드들을 생성했습니다.

공통 부분을 함수로 만들지 않고 클래스로 제작한 이유는 추가적인 로직이 늘어날때 기존에 작성된 TradeClass를 재활용할 수 있다는 점과 다른 계좌에 입금, 출금 기능을 추가한다면 오버라이드를 통해 구현할 수 있다고 생각했기 때문입니다.

거래내역을 생성하고 잔액을 수정하는 작업은 트랜잭션을 사용했습니다.

거래를 진행하다가 해당 계좌의 잔액은 수정되었으나, 서버에 오류가 발생해 중지가 된다면 거래내역이 생기지 않고 데이터의 부정합이 생기기 때문입니다.

그래서 데이터 부정합을 방지하고자 트랜잭션을 사용했습니다. 

트랜잭션 격리수준은 SQLite의 기본으로 설정되어 있는 SERIALIZABLE을 사용했습니다. 

격리수준을  SERIALIZABLE 사용한 이유에 대해서는  9. 개발 과정에서 고민하고 해결한 문제들 에서 자세히 설명하겠습니다.



```python
class Trade:

    def update_account(self, amount, ex_account):
        ex_account.balance = ex_account.balance + amount
        if ex_account.balance < 0:
            return False
        ex_account.save()
        return ex_account

    def create_transaction(self, amount, description, ex_account, t_type):
        transaction_history = Transaction.objects.create(
            account=ex_account,
            amount=amount,
            balance=ex_account.balance,
            t_type=t_type,
            description=description
        )
        return transaction_history

    def check_auth(self, authenticated_user, account_number):
        try:
            ex_account = Account.objects.get(
                account_number=account_number, user=authenticated_user)
            return ex_account
        except Account.DoesNotExist:
            return False

    @transaction.atomic
    def trade(self, ex_account, amount, description, t_type):
        if t_type == "출금":
            amount_after_transaction = self.update_account(
                amount * -1, ex_account)  # 해당 계좌 잔액 수정
        elif t_type == "입금":
            amount_after_transaction = self.update_account(
                amount, ex_account)  # 해당 계좌 잔액 수정

        if amount_after_transaction == False:  # 잔액 부족으로 거래 불가능
            return False
        transaction_history = self.create_transaction(
            amount, description, ex_account, t_type)  # 거래 내역 생성

        data = {
            "거래 계좌": transaction_history.account.account_number,
            "거래 금액": transaction_history.amount,
            "거래 후 금액": transaction_history.balance,
            "거래 종류": transaction_history.t_type,
            "거래 날짜": transaction_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "적요": description
        }
        return data
```

출금을 처리하는 View입니다. 먼저 거래가 되는 금액을 검증하고 계좌가 존재하는지 확인했습니다. 

그리고 Trade 부모 클래스에 정의되어 있는 함수들을 사용해 출금을 처리했습니다.


```python
class WithdrawView(View, Trade):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = str(data['account_number'])
            withdraw_amount = int(data['amount'])
            description = str(data['description'])
            t_type = str(data['t_type'])

            # 거래 금액 확인
            if withdraw_amount <= 0:
                return JsonResponse({'Message': 'AMOUNT_ERROR'}, status=400)
            # 계좌 존재 확인
            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400)

            ex_account = self.check_auth(authenticated_user, account_number)
            if ex_account == False:  # 계좌 권한 확인
                return JsonResponse({'Message': 'AUTH_ERROR'}, status=400)

            data = self.trade(ex_account, withdraw_amount, description, t_type)
            if data == False:  # 거래 가능 확인 및 거래 실시
                return JsonResponse({'Message': 'BALANCE_ERROR'}, status=400)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)

        except ValueError:
            return JsonResponse({'Message': 'AMOUNT ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)

```

#### 거래내역 조회 API

거래내역은 개인정보이니 계좌 소유주만 요청 할 수 있습니다.

거래내역 조회는 거래일시와 입출금을 선택해서 필터링이 가능합니다. 

```python
class ListView(View, Trade):
    @login_decorator  # 해당 계좌, 페이지
    def get(self, request):
        try:
            user = request.user
            account_number = request.GET.get("account_number", None)
            t_type = request.GET.get("t_type", None)
            started_at = request.GET.get("started_at", None)
            end_at = request.GET.get("end_at", None)
            OFFSET = int(request.GET.get("offset", "0"))
            LIMIT = int(request.GET.get("limit", "10"))

            # 해당계좌의 소유주가 맞는지 확인
            ex_account = Account.objects.get(
                account_number=account_number, user_id=user.id)
            if ex_account == None:
                return JsonResponse({'Message': 'AUTH_ERROR'}, status=400)

            filters = self.transaction_list_filter(
                ex_account, started_at, end_at, t_type)

            list_count = Transaction.objects.filter(**filters).count()
            transaction_list = Transaction.objects.filter(
                **filters).order_by("id")[OFFSET:LIMIT]

            results = [{
                '계좌 번호': ex_account.account_number,
                '거래 후 잔액': transaction.balance,
                '금액': transaction.amount,
                '적요': transaction.description,
                '거래 종류': transaction.t_type,
                '거래 일시': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }for transaction in transaction_list]

            return JsonResponse({'Message': 'SUCCESS', 'Data': results, 'TotalCount': list_count}, status=201)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
```

필터링 분기 처리하기 위해 함수를 만들었습니다.

```python
def transaction_list_filter(self, account, started_at, end_at, t_type):
        filters = {'account': account}

        if t_type == "출금":
            filters['t_type'] = "출금"
        elif t_type == "입금":
            filters['t_type'] = "입금"

        if started_at and end_at:
            start_date = datetime.strptime(started_at, '%Y-%m-%d')
            end_date = datetime.strptime(end_at, '%Y-%m-%d')
            end_date = end_date + timedelta(days=1)
            filters['created_at__gte'] = start_date
            filters['created_at__lt'] = end_date

        return filters
```



### 9. 개발 과정에서 고민한 문제들

#### 필터링 분기처리



#### 계좌의 잔액과 거래내역의 잔액이 음수일 경우

- 문제

  테이블에서 계좌의 잔액과 거래 내역의 잔액이 음수로 될 경우 500 에러를 응답함

- 원인

  테이블에  계좌의 잔액과 거래 내역의 잔액 컬럼들을 UNSIGNED INT로 선언했기 때문에 음수가 들어갈 경우 서버 내부 오류를 일으키고 있음 

- 해결

#### 격리수준에 대해 고민

- 문제

- 원인

- 해결

#### 거래내역이 1억건을 넘어서는 경우

- 문제

- 원인

- 해결

### 10. 개발 과정에서 배운 것들 

- 로그인 회원가입 API

<img src = "https://user-images.githubusercontent.com/48669085/148172473-687d4046-8713-4daf-826e-86ef43e3e2b2.png" width="700px">

- 입출금 API

<img src = "https://user-images.githubusercontent.com/48669085/148154942-9b072306-ed23-4b49-bfa4-c16d0833cf21.png" width="700px">

- 거래내역 조회 API

<img src = "https://user-images.githubusercontent.com/48669085/148154966-4b76b389-3825-4383-9be4-62312cbe4dc5.png" width="700px">
