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

데코레이터 함수를 사용해서 사용자를 검증하는 로직을 구현했습니다. 
  
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
사용자가 가지고 있는 계좌만 출금과 입금이 가능합니다. 저는 코드를 작성하기 전에 먼저 출금과 입금의 공통점은 거래라고 생각했습니다.
그래서 공통 부분을 tradeClass를 작성했습니다. 그리고 잔액 수정, 권한을 확인, 거래내역 생성, 잔액 음수 예외처리, 거래가 진행되는 트랜잭션 메소드들을 생성했습니다.

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



#### 거래내역 조회 API

### 9. 사전과제가 요구한 것
<img src = "https://user-images.githubusercontent.com/48669085/148150818-fd921844-42cc-428c-a2fc-c2d644cc55f2.png" width="700px">


### 9. 개발 과정에서 고민하고 해결한 문제들

#### API 보안

#### 계좌의 잔액과 거래내역의 잔액

- 문제

    계좌의 잔액과 거래내역의 잔액의 무결성을 지키고 각각 관리해서 두 잔액의 값이 항상 일치해야함

- 원인
    

- 해결

#### 계좌의 소유주만 요청하는 방법

- 문제

- 원인

- 해결

#### 잔액의 출금을 넘어서는 경우

- 문제

- 원인

- 해결

#### 거래내역이 1억건을 넘어서는 경우

- 문제

- 원인

- 해결

### 10. 개발 과정에서 배운 것들 
<img src = "https://user-images.githubusercontent.com/48669085/148154887-80e0f097-6626-4e65-b63c-6178696bad47.png" width="700px">
<img src = "https://user-images.githubusercontent.com/48669085/148154942-9b072306-ed23-4b49-bfa4-c16d0833cf21.png" width="700px">
<img src = "https://user-images.githubusercontent.com/48669085/148154966-4b76b389-3825-4383-9be4-62312cbe4dc5.png" width="700px">

