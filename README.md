# 8퍼센트

### 1. 과제 안내

1. REST API 기능

   - 거래내역 조회 API
   - 입금 API
   - 출금 API

### 2. 사전 과제에 임하는 나의 로드맵 

<img src = "https://user-images.githubusercontent.com/48669085/148150277-694354fa-5d91-473b-a8fc-156f83cd8f48.png" width="800px">

### 3. 문제 정의

- 문제 

  계좌의 잔액을 별도로 관리할 수 있고, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장할 수 있어야 합니다.

- 문제인식 및 해결 목표

  사용자는 계좌를 생성할 수 있고, 자기의 계좌에만 입출금이 가능하며 거래내역을 생성하고 조회할 수 있는 프로그램 제작

  사용자가 우리의 서비스에 신뢰를 가지고 입출금을 할 수 있도록 프로그램을 제작합니다.

### 4. 문제별 해결 방법

- 계좌 생성

  1. 사용자에게 계좌 생성 요청을 받는다.

  2. 사용자에게 계좌번호와 금액을 입력받는다.

     2.1  금액을 입력하지 않으면 기본적으로 잔액은 0원이다.

     2.2  금액을 입력한다면 금액만큼 입금을 실행한다.

  3. 입금을 실행한다.

  4. 계좌를 생성한다.

- 입금

  1. 사용자에게 (입금할 계좌, 입금할 금액, 적요, 거래 종류)을 입력받는다.

  2. 사용자가 입력한 계좌에 권한이 있는지 확인한다.

     2.1 계좌에 권한이 없다면 권한이 없다고 사용자에게 응답한다.

  3. 계좌의 권한이 있다면 거래를 계속 진행한다.

  4. 해당 계좌의 잔액을 입금한 금액만큼 증가시킨다.

  5.  (입금한 계좌, 입금한 금액, 입금 후 금액, 적요, 거래 종류, 거래 날짜)를 담은 거래내역을 생성한다. 

     5.1 거래내역을 생성하다 서버 오류로인해 실패한다면 계좌의 잔액도 원래대로 되돌리고 거래를 취소한다.

  6. 거래내역의 잔액과 해당 계좌의 잔액을 비교한다.

     6.1 거래내역의 잔액과 해당 계좌의 잔액이 다르다면  거래내역을 지우고 잔액도 원래대로 되돌리고 거래를 취소한다.

  7. 입금을 완료한다.

- 출금

  1. 사용자에게 (출금할 계좌, 출금할 금액, 적요, 거래 종류)을 입력받는다.

  2. 사용자가 입력한 계좌에 권한이 있는지 확인한다.

     2.1 계좌에 권한이 없다면 권한이 없다고 사용자에게 응답한다.

  3. 계좌의 권한이 있다면 거래를 계속 진행한다.

  4. 해당 계좌의 잔액을 출금한 금액만큼 감소시킨다.

     4.1 해당 계좌의 잔액이 출금한 금액보다 작다면 거래를 취소한다.

  5.  (출금한 계좌, 출금한 금액, 출금 후 금액, 적요, 거래 종류, 거래 날짜)를 담은 거래내역을 생성한다. 

     5.1 거래내역을 생성하다 서버 오류로인해 실패한다면 계좌의 잔액도 원래대로 되돌리고 거래를 취소한다.

  6. 거래내역의 잔액과 해당 계좌의 잔액을 비교한다.

     6.1 거래내역의 잔액과 해당 계좌의 잔액이 다르다면  거래내역을 지우고 잔액도 원래대로 되돌리고 거래를 취소한다.

  7. 출금을 완료한다.

     

- 계좌의 잔액과 거래 내역의 잔액을 각각 관리하는 방법

  - 계좌 테이블과 거래내역 테이블을 따로 생성하고 잔액 컬럼도 개별적으로 생성한다.
  - 거래가 완료되면 계좌의 잔액거래과 내역의 잔액은 항상 동일해야 한다.

- 출금과 입금을 할 때  데이터의 무결성을 지키는 방법
  - 트랜잭션을 사용해서 데이터 무결성을 지킨다.
  - 테이블에 제약 조건을 건다.

### 3. 사전 과제가 요구한 것

<img src = "https://user-images.githubusercontent.com/48669085/148150818-fd921844-42cc-428c-a2fc-c2d644cc55f2.png" width="700px">



### 4. 일정 관리



<img src = "https://user-images.githubusercontent.com/48669085/148186741-f3126aab-b11f-4259-8675-0f6b02da1e58.png" width="500px">

### 5. 개발 환경 및 프로젝트 구조

<img src = "https://user-images.githubusercontent.com/48669085/148112357-ccc98696-53e8-46b1-83f9-089fddf7b456.png" width="650px">
    오늘 멘토님한테 물어볼거 -> 

    - python 3.9.1
    - django 4.0
    - sqlite

### 6. 데이터베이스 관계
![image](https://images.velog.io/images/earthkingman/post/d519d304-8cfe-40fd-8ae9-9c3c1418d336/image.png)

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

#### 사용자 권한 확인 방법

사용자의 권한을 확인하는 방법은 세션 쿠키 방식을 사용했습니다. 

토큰 방식과 세션 방식 둘 중 세션을 선택한 이유는 탈취 당했을 때 신속하게 대응할 수 있는 방법은 세션이기 때문입니다.
토큰이 유출된다면 서버에서 대응하는 방법이 어렵습니다. 데이터베이스에 저장된 계좌정보를 바꾸는것이 아닌 이상 토큰의 유효 기간 동안은 악성 유저가 남의 계좌의 돈을 계속 탈취할 수 있는 큰 문제가 생길 수 있습니다. 

하지만 세션 쿠키가 유출된다면 서버에서 세션 정보를 다 삭제하면 됩니다. 물론 사용자는 불편하겠지만, 저는 사용자의 편의성보다는 보안성이 더 중요하다 생각했기 때문에 세션 방법을 사용했습니다. 

try catch가 많이 사용되었습니다. 코드의 가독성이 떨어지고 복잡하지만 계좌를 생성할 때 생기는 예외처리에 대해서 확실하고 꼼꼼하게 처리하고 싶었습니다.  

  ```python
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'Message': 'USER_DOES_NOT_EXIST'}, status=401)

            user = User.objects.get(email=data['email'])
            userList = User.objects.filter(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                request.session['userId'] = user.id  ##세션 쿠키 부분
                return JsonResponse({'Message': "LOGIN_SUCCESS"}, status=200)

            return JsonResponse({'Message': 'INVALID_PASSWORD'}, status=401)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

  ```



#### 계좌 생성 API

계좌를 생성할 때는  사용자로부터 입력받는 계좌번호와 사용자의 정보, 계좌를 개설할 때 넣는 기본 금액 정보를 수집합니다.

계좌 생성 API의 기본 로직은 계좌를 생성한 후 입금을 실행합니다. 

계좌 개설을 한 다음에 입금을 실행했습니다. 

계좌의 잔액과 입금 거래 내역의 잔액을 비교해 데이터 정합성이 깨지는 것을 막고 싶었습니다. 

**궁금한점**

 **정말 운 나쁘게  동일한 계좌 생성요청이 같이 들어왔을 때 한 트랜잭션의 기본 금액은 10억, 또 다른 기본 금액이 0원으로 들어오는 경우**

 **0원이 맞는건데 10억으로 저장될수가 있다. 그래서 거래내역을 따로 남기면 좀 더 장애 대응을 잘 할수있을거라 생각하는데 잘못된 생각인가?**

```python
class AccountView(View):
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            # userId = request.user
            user_id = request.session['userId']
            deposit_amount = validate_amount(data['amount'])
            account_number = validate_account_number(data['account_number'])

            if Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'DUPLICATE_ERROR'}, status=400)
            user = User.objects.get(pk=user_id)
            account = Account.objects.create(
                user=user,
                account_number=account_number,
                balance=0
            )
            if deposit_amount > 0:
                data = trade(account, deposit_amount, "계좌생성", "입금")
            return JsonResponse({'Message': 'SUCCESS'}, status=201)

        except Account.DoesNotExist:
            return JsonResponse({'Message': 'UNIQUE_ERROR'}, status=400)
        except Account.MultipleObjectsReturned:
            return JsonResponse({'Message': 'UNIQUE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

```

#### 출금 및 입금 API

사용자가 가지고 있는 자기의 계좌만 출금과 입금이 가능합니다. 

출금과 입금의 기본적인 로직은 계좌의 잔액을 수정하고 거래내역을 생성한 후 거래내역의 잔액과 계좌의 잔액을 비교합니다.

개발을 진행하다보니 출금과 입금로직에 중복이 되는 로직이 많았습니다. 그래서 중복이 되는 부분은 따로 한 파일에 모으고 필요할 때 호출해서 사용했습니다.

하지만 서버에 오류가 발생한다면  출금, 입금을 진행하다가 해당 계좌의 잔액은 수정되지만, 거래내역이 생기지 않는 데이터 부정합이 생길수 있습니다.  

그래서 부정합을 방지하는 즉 무결성을 지키기 위해 출금,  입금이 이루어지는 내부 로직들을 하나의 트랜잭션으로 묶어서 사용했습니다. 

```python
@transaction.atomic
def trade(ex_account, amount, description, t_type):

    amount_after_transaction = update_account(
        amount, ex_account, t_type)  # 해당 계좌 잔액 수정

    transaction_history = create_transaction(
        abs(amount), description, ex_account, t_type)  # 거래 내역 생성

    if transaction_history.balance != ex_account.balance: # 잔액 비교
        raise BalanceConsistencyException
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

출금을 처리하는 View입니다.  

출금의 경우엔 잔액 부족에 대해 고려해야 합니다. 

잔액 부족은 테이블에 계좌의 잔액과 거래 내역의 잔액 컬럼들을 UNSIGNED INT로 선언했기 때문에 음수가 들어갈 경우 트랜잭션의 일관성 성질에 위반되고 서버 내부 오류 발생하고 있습니다. 

하지만 클라이언트는 명확한 오류를 알 수가 없습니다. 그래서 명확한 에러를 응답해야 하기에 따로 예외처리를 했습니다.

잔액 부족에 대해 트랜잭션 안에서 처리하면 비용이 많이 들거라 예상이 되었기 때문에 트랜잭션 밖에서 처리했습니다


```python
class WithdrawView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.session['userId']
            account_number = validate_account_number(data['account_number'])
            withdraw_amount = validate_amount(data['amount'])
            description = validate_description(data['description'])
            t_type = validate_t_type(data['t_type'])

            if not Account.objects.filter(account_number=account_number).exists():
                return JsonResponse({'Message': 'EXIST_ERROR'}, status=400) # 계좌가 존재하지 않는 경우

            ex_account = check_auth(user_id, account_number) #계좌 권한 조회
            
            if ex_account.balance - withdraw_amount < 0: # 거래 가능 확인
                raise BalanceError
            data = trade(ex_account, withdraw_amount, description, t_type)

            return JsonResponse({'Message': 'SUCCESS', "Data": data}, status=201)

        except ValidationError as detail: #Validation 정의한 조건에 안맞는 경우 
            return JsonResponse({'Message': 'VALIDATION_ERROR' + str(detail)}, status=400)
        except AccountAuthError:#계좌에 권한이 없는 경우
            return JsonResponse({'Message': 'AUTH_ERROR'}, status=403)
        except BalanceError:#잔액이 부족한 경우
            return JsonResponse({'Message': 'BALANCE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'Message': 'ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
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

- 문제

  거래내역 조회를 할 때 필터링을 위해 if문이 난잡하게 사용되고 있습니다.

  ```python
           if t_type != None :
                  transaction_list = Transaction.objects.filter(account_id = ex_account.id, t_type = t_type)
              elif started_at != None and end_at != None:
                  start_date = datetime.strptime(started_at, '%Y-%m-%d')
                  end_date   = datetime.strptime(end_at, '%Y-%m-%d')
                  transaction_list = Transaction.objects.filter(account_id = ex_account.id, created_at__range = (start_date, end_date))
              else :
                  transaction_list = Transaction.objects.filter(account_id = ex_account.id)
  ```

- 이유

  View의 코드가 너무 난잡하고 추가적인 필터링이 생긴다면 계속 if elif else를 사용해야 하는 문제가 생깁니다.

- 해결

  필터링 딕셔너리를 만드는 함수를 만들었습니다. 

  if elif를 사용하지만 기존의 코드보다 가독성이 높아보이고, 따로 함수로 뺏기 때문에 유지보수가 쉽다고 생각했습니다.

  t_type, started_at, end_at에 어떤 값이 오느냐에 따라 정렬이 달라지게 구현되어 있습니다.

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

#### 클래스형 뷰와 함수형 뷰

- 문제

  제가 사용하는 뷰는 총 5개입니다. 

  - User(로그인, 회원가입)
  - Account(계좌 생성),
  - Transaction(입금, 출금, 거래내역 조회)

- 이유

  장고에서 view를 작성하는 방법은 함수형 뷰, 클래스형 뷰 두 가지가 있습니다.
  뷰를 구현할 때 어떤 뷰를 기반으로 구현을 해야 좋을지에 대한 고민을 많이 하였습니다.
  각각의 장단점과 사용 용도를 알고 각 뷰의 역할에 맞는 뷰를 기반으로 구현하고자 하였습니다

- 해결

  함수형 뷰는 Method별로 분기 처리를 해야하는데 이 부분이 번거롭다고 생각했습니다. 클래스형 뷰는 함수이름을 Method명으로 제작하기 때문에 더 깔끔하고 직관적이다고 느껴져서 클래스형 뷰를 사용했습니다.

#### get(), filter() 함수 중 무엇이 적합할까?(미해결 뭐가 더 효율이 좋은지 모르겟음) 

- 문제

  사용자id값으로 사용자를 조회해 계좌의 권한을 확인하거나 계좌번호로 계좌 정보를 확인할 때 get(), filter() 함수 중 어떤 것이 적합한지 고민

- 이유

  - get()메소드 사용

    .get() 메소드 결과값이 2개 이상의 존재하는 경우 djangobin.models.MultipleObjectsReturned를 출력하고, 해당 값이 없으면 djangobin.models.DoesNotExist를 출력합니다. 값

  - filter()메소드 사용

    새로운 쿼리셋을 생성 후, 필터 조건에 부합하는 객체들을 넣은 후 리턴합니다.(즉, 필터조건에 부합하는 객체들이 하나도 없을시, 에러 메시지가 아닌 빈 쿼리셋을 리턴합니다.)

- 해결

  저는 pk처럼 값처럼 고유한 값이 있는 경우엔 get()을 사용하고 
  사용자와 계좌번호는 테이블에 unique키를 걸어놨기 때문에 중복이 허용되지 않습니다. 그래서 조회를 한다면 항상 1개의 값이 나옵니다. 



#### 거래내역이 1억건을 넘어서는 경우 어떻게하면 조회를 빨리 할 수 있을까?

- 문제


  조회는 거래내역이 1억건을 넘어선다면 속도가 매우 느려지기 때문에 빠르게 검색할 수 있는 방법을 찾아야 합니다.

- 이유

  - 조회 속도가 느려지는 이유

    문제를 해결하기 위해 그 문제에 대해 먼저 파악했습니다. 기본적으로 인덱스를 생성하지 않으면 전체 테이블 스캔(Full Table Scan)을 진행합니다.

    테이블에 존재하는 모든 데이터를 읽어가면서 조건에 맞으면 결과로서 추출하고 조건에 맞지 않으면 버리는 방식으로 진행되기 때문에 속도가 느립니다.

  - 전체 테이블 스캔(Full Table Scan)를 하는 경우는 언제인가?

    적용 가능한 인덱스가 없는 경우입니다. 

  - 전체 테이블 스캔(Full Table Scan)의 단점을 보완하기 위한 방법은?

    스캔기법의 단점을 보완하기 위해 등장한 것이 인덱스입니다. 인덱스를 사용하면 데이터 검색 시, 먼저 인덱스 파일에서 찾고자하는 데이터가 저장된 주소를 찾고 그 뒤 찾은 주소값을 통해 데이터 파일에서 데이터를 찾기 때문에 속도가 빠릅니다.

- 해결

  멀티 컬럼 인덱스를 생성했습니다.

  ```python
  class Transaction(models.Model):
      account = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
      balance = models.PositiveBigIntegerField(null=False, validators=[validate_balance])
      amount = models.PositiveBigIntegerField(null=False, validators=[validate_amount])
      t_type = models.CharField(max_length=2, null=False,validators=[validate_type])
      description = models.CharField(max_length=50, null=False)
      created_at = models.DateTimeField(auto_now_add=True)
  
      class Meta:
          db_table = 'transaction_index_history'
          indexes = [
              models.Index(fields=['account_id', 't_type']),
              models.Index(fields=['account_id', 'created_at']),
          ]
  
  ```

  인덱스를 생성하고 성능을 테스트해봤습니다.

  **데이터 약 오백만 개**

| 검색 조건   | 인덱싱 전 속도 | 인덱싱 후 속도 |
| ----------- | -------------- | -------------- |
| 기본        | 1070ms         | 212ms          |
| 날짜로 검색 | 1965ms         | 715ms          |
| 입출금 검색 | 1070ms         | 203ms          |

테스트 결과 내용은 [상세보기](https://velog.io/@earthkingman/20211230%EC%9D%B8%EB%8D%B1%EC%8B%B1-%EB%A7%A4%EA%B8%B0%EA%B8%B0-wuu1y4ik) 를 참고해주세요



#### 트랜잭션을 사용할 때 적합한 방법

- 문제

  - 데코레이터를 사용한 트랜잭션
  - with 명령어를 이용한 트랜잭션
  - savepoint을 직접 지정해 주는 트랜잭션 

- 이유

  트랜잭션을 사용하는 방법을 여러가지가 있고 각 상황에 알맞는 방법이 있습니다.

- 해결

  

  

### 10. 아직 미숙하고 고쳐야 할 점

- 제 코드의 문제는 try catch 부분이 너무커서 에러가 난다면 어느부분에서 에러가 정확하게 나는지 알 수가 없습니다.
  - 어떻게 하면 코드를 효율적으로 관리할 수 있을지 고민을 했지만 실력 부족과 파이썬 미숙으로 해결하지 못했습니다.



## 11. 과제가 끝나고 공부해야 하는 내용

#### 추후에 다른 사람 계좌에 출입금이 가능할 때 격리수준

트랜잭션 격리수준은 SQLite의 기본으로 설정되어 있는 SERIALIZABLE을 사용했습니다. 

- 문제

  은행 출금 입금의 적합한 격리 수준 찾기

- 이유

  트랜잭션의 격리수준은 4가지가 있습니다.

  - Read Uncommitted

    - SELECT 문장이 수행되는 동안 해당 데이터에 shared lock이 걸리지 않는 계층.

    - 트랜잭션이 처리중이거나, 아직 COMMIT 되지 않은 데이터를 다른 트랜잭션이 읽는 것을 허용

  - Read Comitted

    - SELECT 문장이 수행되는 동안 해당 데이터에 shared lock이 걸리는 계층.
    - 트랜잭션이 수행되는 동안 다른 트랜잭션이 접근할 수 없어 대기
    - COMMIT이 이루어진 트랜잭션만 조회 가능하도록 허용함으로써 Dirty Read를 방지해줍니다. 하지만 COMMIT된 데이터만 읽더라도 Non-Repeatable Read와 Phantom Read 현상을 막지는 못합니다. 

  - Repeatable Read

    - 트랜잭션이 완료될 때까지 SELECT 문장이 사용하는 모든 데이터에 shared lock이 걸리는 계층.
    - 트랜잭션이 범위 내에서 조회한 데이터의 내용이 항상 동일함을 보장
    - Phantom Read 현상을 막지는 못함

  - Serializable

    - 모든 작업을 하나의 트랜잭션에서 처리하는 것과 같은 가장 높은 고립 수준

- 해결
  Repeatable Read를 사용합니다.

  - Read Uncommitted는 Dirty Read가 발생합니다.

    입금을 가정해 보겠습니다.  A 트랜잭션에서 A의 계좌에서 10만원에서 11만원으로 변경합니다.

  Read Comitted는 읽는 시점에 따라 결과가 다를 수 있기 때문에 사용하지 않았습니다.
  Serializable는 동시성 처리가 너무 떨어집니다. 하지만 
