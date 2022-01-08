### 1. 과제 안내

1. REST API 기능

   - 거래내역 조회 API
   - 입금 API
   - 출금 API

### 2. 문제 정의

- 문제 

  계좌의 잔액을 별도로 관리할 수 있고, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장할 수 있어야 합니다.

- 해결 목표

  사용자는 계좌를 생성할 수 있고, 자기의 계좌에만 입출금이 가능하며 거래내역을 생성하고 조회할 수 있는 프로그램 제작

  사용자가 우리의 서비스에 신뢰를 가지고 입출금을 할 수 있도록 프로그램을 제작합니다.

### 3. 문제별 해결 방법

#### 보안

- 로그인 과정

![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59ulN3Eg-qxtipTmSK54GF9fYIM92Ob5gS2vTyqhNapQ-MRUHCKtiwS2bAMc5EYy7PMpvlP4rvjQ7Wph_NDt2qAhoVCU3DjYyARUHslkwOelDgqzysi3LmmGr2iUpDtuklkhL2hTEtWubxX8HgEoScfnSKA8VdPgNaw2a6fQKMfnHaGhgR2wmrpNktenEf6LAKARnO0dRMK2Ej1Cf0G0ScqR7orUIiNLsfESIgA_nJUJEruFM4Er5TOjNOlUTkpWYirBuNB0KW00ne0)

- 토큰 검증 과정

  ![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59ulN3Eg-qxtipTmSK54GF9fYIM92Ob5gS2vHq3F1NUp9hoPjDQhiIS4eMtRGlUDcvGUBMfuSsokGflMZQ-shmLeH5Xh6DoScfniK98VdPg7bGrTlDVzsvuCtVBsvODC5jWSYZ6lPaxyNKtiaLGdrZ1dC2LcbESYkwwxYLlUrPmOT45aqhDI-5o01B0i040)

- 토큰 재발급 과정(성공)

  ![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59m3F1KU3DhofjDQxaWOgYooScfnSKA8VdPgNaAhvVtl5xSe_1svjGtStSWgOQQQWLJy6RknDVTMx5P5fIQLfHQd04rxys2bZTj2pLGxTWmvzMEJgYBD94iIKaiIKnAB4x5D6NXXhUpUhXWyhZjWxaB8ej7tQjD3M-MpGKwfL_XzSwMLridA63JuvTQhe35wTZ21Q4CuGg7rBmKO9G00000)

  

#### 계좌 생성

![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59ujRdbpQAUrviwtixOyMPcWyAh7HrlfYvyCxT5uSs2bZTj2xaISqem1DzEdQFmQjFUDxCsS44C0XcPabYIc9HOd0etLE5DyzmtBHkvO18ezhwPE_5rzrRisj_CQmNQgA3nQkE6r_Dcl6xQycRwMgXXcaIQ1l4fK0QevzNchLnSgJb0BPZ-cF5cUOF2cwbTR-OsKEWZmcv8pKlXSW0Im9W00000)



#### 입금

![PlantUML diagram](http://www.plantuml.com/plantuml/png/ZP4_JiCm6CLtd-8x05o00PKxS06JUa248CM6kK2e8fe1f4G95QbIX10BKjC_g0iNib_km3T4KOOCNVmDx_dt_FoDj96XkRtsXUTVgi3GyIbf5Twfa4x8RY9y96uTDyKURnF2uidkuoQhY0UovH6XkiSyvH5XkXJjnJxYpFEKrdH-SwK2iki9laeXVTEYaR-G_KsQx1tbbl6nUqxPzOVvgWSRIoClf5RTYzYPSZmXBb1bejFxmIXVtMmtI6bxaArNRb6uXoto7y9ZYQW-aDN-5IjHRJSxeNojXYlbqw5AFS3iiqc-XGh6OiG7B-8V)



#### 출금

![PlantUML diagram](http://www.plantuml.com/plantuml/png/ZP9FIiD06CNtSuhl07e15rBlu0LYEminHiX4rr532JOBXOIafGc9YEX2QFedPEE5PbxkuA13YH3GpNoBzxxVntlCI7YMwrrVscnidtF7eyDZ4jozuIuTaTm4U8xKEkoo5dEVq2nb6tP9INeWgGu8vIqMiHu1fXKpYtt4oNZCXQ3Jgmlka5pxUCqPispFi94-acoYBbaYtnAAK3t4slQ9nUh7XYBMXxx5vbqrWNOQVU2QSNVp17dRqoUMPvrPWkyZ6ICXp50cRA__OkLFQhORf9WYIDOhLMJgRelqWt2V8wZ_oJ9bQoMevMR76BS5xuLLZO-g7WhRMvszTD4RCxk3VQPJq-SV2EvCs4W_-Xzy0G00)

#### 계좌의 잔액과 거래 내역의 잔액을 각각 관리하는 방법

- 계좌 테이블과 거래내역 테이블을 따로 생성하고 잔액 컬럼도 개별적으로 생성한다.



#### 출금과 입금을 할 때 잔액을 안전하게 관리하는 방법

- 테이블에 제약 조건을 걸어 데이터 무결성을 지킵니다.
- 트랜잭션을 사용해 계좌의 잔액 과 거래 내역의 잔액은 항상 동일하게 유지합니다.

#### 동시에 입출금 요청이 들어오는 경우에 대해 데이터 동기화

해결하지 못했습니다. 



웹어플리케이션의 관점에서 동기화를 해야할 지 데이터베이스 트랜잭션의 격리성에 맡겨야 하는지
어떤식으로 락을 잡을지에 대한 문제와 락을 잡을 시점과 서버 코드 시점으로 ~ 시언어처럼 락을 거는게 맞는건지 이 부분은 해결하지를 못했다. 데이터베이스의 격리성을 맡겨야하는지

### 4. 개발 환경 및 프로젝트 구조

<img src = "https://user-images.githubusercontent.com/48669085/148112357-ccc98696-53e8-46b1-83f9-089fddf7b456.png" width="650px">

    - python 3.9.1
    - django 4.0
    - sqlite 3.0

### 5. ER-D

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
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── wsgi.py
│
└── manage.py

```

### 7. API 명세

### 8. 개발 과정에서 고민한 문제들

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

#### get(), filter() 함수 중 무엇이 적합할까?

- 문제

  사용자id값으로 사용자를 조회해 계좌의 권한을 확인하거나 계좌번호로 계좌 정보를 확인할 때 get(), filter() 함수 중 어떤 것이 적합한지 고민

- 이유

  - get()메소드 사용

    .get() 메소드 결과값이 2개 이상의 존재하는 경우 djangobin.models.MultipleObjectsReturned를 출력하고, 해당 값이 없으면 djangobin.models.DoesNotExist를 출력합니다.

  - filter()메소드 사용

    새로운 쿼리셋을 생성 후, 필터 조건에 부합하는 객체들을 넣은 후 리턴합니다.(즉, 필터조건에 부합하는 객체들이 하나도 없을시, 에러 메시지가 아닌 빈 쿼리셋을 리턴합니다.)

- 해결
  pk를 조건으로 사용할 때는 get()을 사용하고 pk를사용하지 않는다면 filter를 사용했습니다.

#### 거래내역이 1억건을 넘어서는 경우 어떻게하면 조회를 빨리 할 수 있을까?

- 문제


  조회는 거래내역이 1억건을 넘어선다면 속도가 매우 느려지기 때문에 빠르게 검색할 수 있는 방법을 찾아야 합니다.

- 이유

  거래내역 1억건이 넘어서면 수 많은 문제들이 생깁니다. 그 많은 문제 중 조회에 초점을 두었습니다.

  이유는 사용자들이 입금과 출금보다는 거래내역을 더 자주 조회한다고 생각했습니다. 저 또한 출입금 횟수보다 월급이 들어오는지 안들어오는지 거래내역을 확인하는 경우가 더 많았습니다.

- 해결

  멀티 컬럼 인덱스를 생성했습니다.

  인덱싱을 생성하니 조회를 제외한 삭제, 수정, 삽입의 속도는 느려졌지만, 조회의 속도가 확실하게 개선되었습니다.

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

### 9. 아직 미숙하고 고쳐야 할 점

- 제 코드의 문제는 try catch 부분이 너무커서 에러가 난다면 어느부분에서 에러가 정확하게 나는지 알 수가 없습니다.
  - 어떻게 하면 코드를 효율적으로 관리할 수 있을지 고민을 했지만 실력 부족과 파이썬 미숙으로 해결하지 못했습니다.


- 공유 자원인 잔액에 동시에 접근한다면 금액 오류가 발생합니다.

  - 동기화가 제대로 일어나지 않는다면 잔액의 손실이 발생합니다..

    테스트를 진행했습니다.   curl 명령어를 사용해 입금과 출금을 10000번을 동시에 실행해보았습니다. 

    ![image-20220108030353786](/Users/ji-park/Library/Application Support/typora-user-images/image-20220108030353786.png)







### 10. 과제가 끝나고 공부해야 하는 내용


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
