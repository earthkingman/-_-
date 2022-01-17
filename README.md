## 1. 과제 안내

1. REST API 기능

   - 거래내역 조회 API
   - 입금 API
   - 출금 API

2. 배포주소 : http://13.209.65.161

3. Localhost에서 돌리는 방법

   Django 버전이 4.0이라서 Python 3.8 부터 가능합니다.

   - 프로젝트 설치

     ```shell
     $ git clone https://github.com/earthkingman/8Percent
     ```

   - 가상환경 생성 및 접속 및 모듈 설치

     ```shell
     $ virtualenv 8percent
     $ cd 8percent
     $ source bin/activate
     ## ~/8Percent/project
     pip install -r requirements.txt
     ```

   - 설정 파일 생성 ()

     ```shell
     ## ~/8Percent/project 
     $ vim my_settings.py
     	SECRET =  "park"
     ```

   - 데이터 베이스 설정

     ```sh
     $ python manage.py makemigrations  
     $ python manage.py migrate                                         
     ```

   - 서버 실행

     ```shell
     $ python manage.py runserver 
     ```

   - 테스트 코드 커버리지 확인 방법

     ```shell
     $ pip install covarage
     $ coverage run manage.py test
     $ coverage html
     ```

     

     <img src = "https://images.velog.io/images/earthkingman/post/9861da11-b649-4385-9fbc-f66511467c40/image.png" width="300px">

## 2. 문제 정의

- 문제 

  계좌의 잔액을 별도로 관리할 수 있고, 계좌의 잔액과 거래내역 잔액의 무결성을 보장할 수 있어야 합니다.

- 해결 목표

  사용자는 계좌를 생성할 수 있고, 자기의 계좌에만 입출금이 가능하며 거래내역을 생성하고 조회할 수 있는 프로그램 제작

## 3. 문제별 해결 방법

#### API 보안 

- 로그인 과정

![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59ulN3Eg-qxtipTmSK54GF9fYIM92Ob5gS2vTyqhNapQ-MRUHCKtiwS2bAMc5EYy7PMpvlP4rvjQ7Wph_NDt2qAhoVCU3DjYyARUHslkwOelDgqzysi3LmmGr2iUpDtuklkhL2hTEtWubxX8HgEoScfnSKA8VdPgNaw2a6fQKMfnHaGhgR2wmrpNktenEf6LAKARnO0dRMK2Ej1Cf0G0ScqR7orUIiNLsfESIgA_nJUJEruFM4Er5TOjNOlUTkpWYirBuNB0KW00ne0)

- 토큰 검증 과정 

  ![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59m3F1KU3DhofjDQxcu888eqc_R5hnjtA3mQbF3csLpkH9pIg1CXJSj6rzjtega9IMn934fiJWLgEbrxuOtSxUyRTa0CnacXp0QHT7SYQ-xaOs2EjCAgXrcLsfESIhS-kubRtjMuDO3Kv2QbyBb02I0lWS0)

- 토큰 재발급 과정(성공)

  ![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59m3F1KU3DhofjDQxaWOgYooScfnSKA8VdPgNaAhvVtl5xSe_1svjGtStSWgOQQQWLJy6RknDVTMx5P5fIQLfHQd04rxys2bZTj2pLGxTWmvzMEJgYBD94iIKaiIKnAB4x5D6NXXhUpUhXWyhZjWxaB8ej7tQjD3M-MpGKwfL_XzSwMLridA63JuvTQhe35wTZ21Q4CuGg7rBmKO9G00000)

  

#### 계좌 생성

![PlantUML diagram](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuKhEoKpDAr7GjLCeJYqgIorIi59ujRdbpQAUrviwtixOyMPcWyAh7HrlfYvyCxT5uSs2bZTj2xaISqem1DzEdQFmQjFUDxCsS44C0XcPabYIc9HOd0etLE5DyzmtBHkvO18ezhwPE_5rzrRisj_CQmNQgA3nQkE6r_Dcl6xQycRwMgXXcaIQ1l4fK0QevzNchLnSgJb0BPZ-cF5cUOF2cwbTR-OsKEWZmcv8pKlXSW0Im9W00000)



#### 입금

![PlantUML diagram](http://www.plantuml.com/plantuml/png/ZP4_JiCm6CLtd-8x05o00PKxS06JUa248CM6kK2e8fe1f4G95QbIX10BKjC_g0iNib_km3T4KOOCNVmDx_dt_FoDj96XkRtsXUTVgi3GyIbf5Twfa4x8RY9y96uTDyKURnF2uidkuoQhY0UovH6XkiSyvH5XkXJjnJxYpFEKrdH-SwK2iki9laeXVTEYaR-G_KsQx1tbbl6nUqxPzOVvgWSRIoClf5RTYzYPSZmXBb1bejFxmIXVtMmtI6bxaArNRb6uXoto7y9ZYQW-aDN-5IjHRJSxeNojXYlbqw5AFS3iiqc-XGh6OiG7B-8V)



#### 출금

![PlantUML diagram](http://www.plantuml.com/plantuml/png/ZP9FIiD06CNtSuhl07e15rBlu0LYEminHiX4rr532JOBXOIafGc9YEX2QFedPEE5PbxkuA13YH3GpNoBzxxVntlCI7YMwrrVscnidtF7eyDZ4jozuIuTaTm4U8xKEkoo5dEVq2nb6tP9INeWgGu8vIqMiHu1fXKpYtt4oNZCXQ3Jgmlka5pxUCqPispFi94-acoYBbaYtnAAK3t4slQ9nUh7XYBMXxx5vbqrWNOQVU2QSNVp17dRqoUMPvrPWkyZ6ICXp50cRA__OkLFQhORf9WYIDOhLMJgRelqWt2V8wZ_oJ9bQoMevMR76BS5xuLLZO-g7WhRMvszTD4RCxk3VQPJq-SV2EvCs4W_-Xzy0G00)

#### 계좌의 잔액과 거래 내역의 잔액을 각각 관리하는 방법

- 계좌 테이블과 거래내역 테이블을 따로 생성하고 잔액 컬럼도 개별적으로 생성합니다.



#### 출금과 입금을 할 때 잔액을 안전하게 관리하는 방법

- 테이블에 제약 조건을 걸어 데이터 무결성을 지킵니다.
- 트랜잭션을 사용해 계좌의 잔액과 거래 내역의 잔액은 항상 동일하게 유지합니다.



#### 동시에 입출금 요청이 들어오는 경우

- 동시에 요청이 들어온다면 요청을 직렬화하지 못했습니다. 
- 정상적으로 출금과 입금이 안되면 오류를 반환해 클라이언트에게 알려주기로 정했습니다. 
- 데이터베이스를 mysql로 변경해 정확한 금액을 얻을 수 있었습니다. (추가)

## 4. 구현 사항

| 기능          | 구현사항                                  | 구현 여부 |
| :------------ | :---------------------------------------- | :-------: |
| 거래내역 조회 | 계좌의 소유주만 거래내역 조회 가능        |    OK     |
|               | 거래내역 시간별로 필터링 하여 조회        |    OK     |
|               | 출금, 입금, 전체 필터링하여 거래내역 조회 |    OK     |
|               | 거래내역 페이지네이션                     |    OK     |
| 입금          | 계좌의 소유주만 자신의 계좌에 입금 가능   |    OK     |
|               | 계좌의 입금 거래내역 생성                 |    OK     |
|               | 입금시 계좌의 잔액 변경                   |    OK     |
| 출금          | 계좌의 소유주만 자신의 계좌에서 출금 가능 |    OK     |
|               | 계좌의 출금 거래내역 생성                 |    OK     |
|               | 출금시 계좌의 잔액 변경                   |    OK     |
|               | 계좌의 잔액 내에서만 출금 가능            |    OK     |



## 5. 개발 환경 및 프로젝트 구조

<img src = "https://user-images.githubusercontent.com/48669085/148770760-b9ab6029-9005-4661-b0e6-6b31471d3c69.png" width="650px">

```
- python 3.9.1
- django 4.0
- sqlite 3.0
```



## 6. ER-D

![image](https://images.velog.io/images/earthkingman/post/d519d304-8cfe-40fd-8ae9-9c3c1418d336/image.png)



## 7. 디렉토리 구조

```bash
├── Makefile
├── README.md
├── bank
│   ├── account
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── error.py
│   │   ├── validation.py
│   │   ├── urls.py
│   │   └── migrations
│   │ 
│   ├── transaction
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── error.py
│   │   ├── validation.py
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
│   │   ├── error.py
│   │   ├── validation.py
│   │   ├── urls.py
│   │   └── views.py
│   └── wsgi.py
│
└── manage.py

```



## 8. 서비스 구조



<img src="https://images.velog.io/images/earthkingman/post/b95d1307-1d42-49e4-9dbb-07ae0d6cf51d/image.png" height="800px" width="800px">



## 9. API 명세 및 테스트 방법

[API 명세서](https://documenter.getpostman.com/view/10344809/UVXgKwvV)

- 상단의 API 명세서를 누르시고 그림 오른쪽 상단에 있는 Run in Postman을 클릭해주세요

<img src="https://user-images.githubusercontent.com/48669085/148824271-7f1f1e09-c187-46bf-a8e0-b22545c35b84.png"  width="650px">

- My Workspace에 추가해주세요

<img src="https://user-images.githubusercontent.com/48669085/148824240-7eaf5551-4dcd-4e5d-8cae-a3f21ac10cc8.png"  width="650px">

- Postman for Mac을 클릭해주세요.

<img src="https://user-images.githubusercontent.com/48669085/148824255-9fe1222b-59ff-4489-a59a-f1ac5f2289a7.png"  width="650px">

- 편의를 위해 만료기간이 없는 토큰들을 적용해놓았습니다. 

![image-20220112002237872](/Users/ji-park/Library/Application Support/typora-user-images/image-20220112002237872.png)



## 10. API 설명

### (로그인) POST /users/login 

- Body

  `email` 과 `password` 는 필수입니다.

  ``` 
  {
      "email":[이메일], 
      "password":[비밀번호] 
  }
  
  예시)
  {
      "email":"test1@8Percent.com",
      "password":"123"
  }
  ```

  



### (회원가입) POST /users/signup 

- Body

  `email` 과 `password` 는 필수입니다.

  ``` 
  {
      "email":[이메일],
      "password":[비밀번호]
  }
  
  예시)
  {
      "email":"test1@8Percent.com",
      "password":"123"
  }
  ```

  

###  (계좌 조회) GET accounts/account

- Headers

  `Authorization` 은 필수입니다.

  ``` 
  Authorization : [발급받은 토큰]
  
  예시)
  Authorization : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.wYWgGA_2Tn-aTiD8UoQFPpT0paJr-1KT-xMUqSQU7qg
  ```

- Query Parameters

  `account_number`  필수입니다.

  ``` 
  ?account_number=[계좌 번호]
  
  예시)
  http://13.209.65.161/accounts/account?account_number=계좌번호1004
  ```



### (계좌 생성) POST accounts/account

- Header

  `Authorization` 은 필수입니다.

  ``` 
  Authorization : [발급받은 토큰]
  
  예시)
  Authorization : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.wYWgGA_2Tn-aTiD8UoQFPpT0paJr-1KT-xMUqSQU7qg
  ```

- Body

  `account_number` 과 `amount` 는 필수입니다.

   `amount` 는 0보다 커야합니다.

  ``` 
  {
      "account_number":[계좌 번호],
      "amount":[금액]
  }
  
  예시)
  {
      "account_number":"계좌번호1007",
      "amount":1000
  }
  ```

  

### (입금) POST transaction/deposit

- Header

  `Authorization` 은 필수입니다.

  ``` 
  Authorization : [발급받은 토큰]
  
  ex)
  Authorization : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.wYWgGA_2Tn-aTiD8UoQFPpT0paJr-1KT-xMUqSQU7qg
  ```

- Body

  `account_number` , `amount`, `description`는 필수입니다.

   `amount` 는 0보다 커야합니다.

  ``` 
  {
      "account_number":[계좌 번호],
      "amount":[금액],
   	  "description": [적요]
  }
  
  예시)
  {
      "account_number":"계좌번호1004",
      "amount":100,
      "description": "월급"
  }
  ```



### (출금) POST transaction/withdraw

- Header

  `Authorization` 은 필수입니다.

  ``` 
  Authorization : [발급받은 토큰]
  
  예시)
  Authorization : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.wYWgGA_2Tn-aTiD8UoQFPpT0paJr-1KT-xMUqSQU7qg
  ```

- Body

  `account_number` , `amount`, `description`는 필수입니다.

   `amount` 는 0보다 커야합니다.

  ``` 
  {
      "account_number":[계좌 번호],
      "amount":[금액],
   	  "description": [적요]
  }
  
  예시)
  {
      "account_number":[계좌 번호],
      "amount":[금액],
   	  "description": [적요]
  }
  ```



### (거래 내역 조회) GET ransaction/list

- Header

  `Authorization` 은 필수입니다.

  ``` 
  Authorization : [발급받은 토큰]
  
  예시)
  Authorization : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.wYWgGA_2Tn-aTiD8UoQFPpT0paJr-1KT-xMUqSQU7qg
  ```

- Query Parameter (일반조회)

  `account_number, ` 계좌번호는 필수입니다.

  `limit` 필수가 아니고 보내지 않는다면 10이 기본값입니다.

  `offset` 필수가 아니고 보내지 않는다면 0이 기본값입니다. 

  ``` 
  ?account_number=[계좌 번호]&limit=[최대 범위]&offset=[시작 인덱스]
  
  예시)
  http://13.209.65.161/transaction/list?account_number=계좌번호1234&limit=0&offset=10
  ```

- Query Parameter (입출금, 날짜 조회)

  `started_at` ,`end_at` 필수입니다. 양식은 [YYYY-MM-DD]입니다.

  `transaction_type` 필수입니다. `입금`, `출금`을 선택하시면 됩니다.

  ``` 
  ?account_number=[계좌 번호]&limit=[최대 범위]&offset=[시작 인덱스]&started_at=[시작 날짜]&end_at=[종료 날짜]&transaction_type=[거래 종류]
  
  예시)
  http://13.209.65.161/transaction/list?account_number=계좌번호1234&limit=0&offset=10&started_at=2022-01-10&end_at=2022-01-12&transaction_type=출금
  
  http://13.209.65.161/transaction/list?account_number=계좌번호1234&limit=0&offset=10&started_at=2022-01-10&end_at=2022-01-12&transaction_type=입금
  ```

- Query Parameter (입출금 조회)

  ``` 
  ?account_number=[계좌 번호]&limit=[최대 범위]&offset=[시작 인덱스]&transaction_type=[거래 종류]
  
  예시)
  http://13.209.65.161/transaction/list?account_number=계좌번호1234&limit=0&offset=10&transaction_type=출금
  
  http://13.209.65.161/transaction/list?account_number=계좌번호1234&limit=0&offset=10&transaction_type=입금
  ```

- Query Parameter (날짜 조회)

  ``` 
  ?account_number=[계좌 번호]&limit=[최대 범위]&offset=[시작 인덱스]&started_at=[시작 날짜]&end_at=[종료 날짜]
  
  예시)
  http://13.209.65.161/transaction/list?account_number=계좌번호1004&limit=10&offset=0&started_at=2022-01-10&end_at=2022-01-12
  ```



## 11. 도전했지만 완벽하게 해결하지 못한 부분

#### 동시성 문제 해결

- 문제

  잔액에 동시에 접근했을 때 금액 오류가 발생합니다.

- 목표

  트랜잭션을 직렬화 해서 동시성 문제를 해결합니다.

  ![](https://images.velog.io/images/earthkingman/post/92383ca7-2236-4471-a24f-14946fe1916f/image.png)

  #### 방법 1. 트랜잭션을 사용한 직렬화

  계좌 1004번은 10000원을 가지고 있습니다.

- 출금 코드 

```python
    @transaction.atomic
    def withdraw(self, account_number, amount, description):
        account = Account.objects.get(account_number=account_number)
        # 계좌 잔액 수정
        account.balance = account.balance - amount
        account.save()
        # 거래 내역 생성
        transaction_history = self.create_transaction(
            amount, description, account, WITHDRAW)  # 거래 내역 생성

        return transaction_history
```

![](https://images.velog.io/images/earthkingman/post/e3493183-9176-48e4-b128-7f0122a8ff3c/image.png)



계좌 1004번에 입금과 출금을 100원을  동시에 10000번 요청했습니다.



- 입금

  ```sh
  for ((i = 0; i < 10000; i++)); do
  curl --location --request POST 'http://localhost:8000/transaction/deposit' \
  --header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjQxNjI2OTQ4fQ.-wG1evB0gfzevQMhHBMI6DOztQIy8p3edCZ1gcYMayw' \
  --header 'Content-Type: application/json' \
  --header 'Cookie: Cookie_2=value; Cookie_3=value; access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OSwiaWF0IjoxNjI5OTEzMjI1LCJleHAiOjE2Mjk5MTY4MjV9.A2Q440G_ENfm8jrVBE1W8tNcqSNUnkYa2FJEq3TPOfU' \
  --data-raw '{
      "account_number":"계좌번호1004",
      "amount":"100",
      "description": "월급"
  }'
  done
  ```

  

- 출금

  ```shell
  for ((i = 0; i < 10000; i++)); do
  	echo $i
  
  curl --location --request POST 'http://localhost:8000/transaction/withdraw' \
  --header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjQxNjI2OTQ4fQ.-wG1evB0gfzevQMhHBMI6DOztQIy8p3edCZ1gcYMayw' \
  --header 'Content-Type: application/json' \
  --header 'Cookie: Cookie_2=value; Cookie_3=value; access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OSwiaWF0IjoxNjI5OTEzMjI1LCJleHAiOjE2Mjk5MTY4MjV9.A2Q440G_ENfm8jrVBE1W8tNcqSNUnkYa2FJEq3TPOfU' \
  --data-raw '{
      "account_number":"계좌번호1004",
      "amount":100,
      "description": "카드값"
  }'
  
  
  done
  ```

- 첫번째 결과

  출금 금액 부족으로 중단

  ![](https://images.velog.io/images/earthkingman/post/37b4bcd9-3d13-465f-8d83-5bc3b4680b88/image.png)

- 두번째 결과

  서버 내부 에러가 발생하지 않았습니다. 

  9500원

  ![](https://images.velog.io/images/earthkingman/post/3ad2743c-a10c-4159-95e0-6a3e0236e87d/image.png)

- 결론

  ![](https://images.velog.io/images/earthkingman/post/4385f7dc-501c-4a05-9367-aae975128fca/image.png)

  sqlite의 격리수준은 Serializable로 가장 높은 격리수준을 가지고 있습니다. 

  저는 한 트랜잭션에서 사용되는 자원들이 처리가 되고 있을 경우 데이터베이스에서 지정한 격리수준에 맞게

  다른 트랜잭션들이 접근하면 처리가 끝날 때까지 대기시키는 것으로 알고 있었습니다.

  근데 실제로 실행해보니 데이터 동기화가 제대로 이루어지지 않아서 500원이라는 손해를 보게 되었습니다. 

  동시성 문제를 해결하지 못했습니다.

  

#### 방법 2. select_for_update을 사용해 락을 거는 방법

row lock을 제어하는 방식으로 DBMS 전체나 table에 lock을 거는 것보다 좁은 범위에 lock을 사용하여 성능 하향을 최소화

![](https://images.velog.io/images/earthkingman/post/d3c0bb3d-c7b9-4cb6-864b-41c0e20bacfb/image.png)

- 변경한 출금 코드

  ```python
    # nowait=False 조회하고자 하는 데이터에 락이 잡혀있는 경우에 락이 풀릴 때까지 대기 (default)
    # nowait=True 조회한 데이터가 락이 잡혀있다면 에러 발생  
    # 출금 (트랜잭션)
      @transaction.atomic
      def withdraw(self, account_number: str, amount: int, description: str) -> dict:
          try:
              # 계좌 잔액 수정
              account = Account.objects.select_for_update(
                  nowait=False).get(account_number=account_number)
              account.balance = account.balance - amount
              account.save()
              # 거래 내역 생성
              transaction_history: Transaction = self.create_transaction(
                  amount, description, account, WITHDRAW)  # 거래 내역 생성
  
              data = self.obj_to_data(transaction_history)
              return data
          except Account.DoesNotExist:
              raise ExitsError
  ##        except OperationalError:  추가된 코드
  ##           raise LockError
  ```

  

  계좌 1004번에 입금과 출금을 100원을  동시에 10000번 요청했습니다.

  ![](https://images.velog.io/images/earthkingman/post/29a90e53-6c9f-4e5d-a27f-2785050de5c7/image.png)

  

  서버 로그를 보니 데이터베이스를 다른 프로그램을 통해 조회 또는 수정중이었기 때문에 오류가 발생했습니다.

  ![img](https://camo.githubusercontent.com/9b577e4cefd08820b10fc647806a5a6a292020759be8f65a7185bb72d3a9071e/68747470733a2f2f696d616765732e76656c6f672e696f2f696d616765732f65617274686b696e676d616e2f706f73742f37333930323333632d366337312d343064632d383430312d3037666266366161653237392f696d6167652e706e67)

  ```python
    except OperationalError:  추가된 코드
          raise LockError
  ```

  락을 예외처리하고 다시 한번 더 진행해보았습니다. 시간이 오래걸려서 10000원에 100원씩 30번 입출금 요청을 했습니다.  

  결과는 출금 취소 11번 입금 취소 5번입니다.

  ![](https://images.velog.io/images/earthkingman/post/a4adb82d-1aa8-413a-8229-a5d30a908e7a/image.png)

![](https://images.velog.io/images/earthkingman/post/144246be-fd34-4f30-aa46-5ff2eb7c0202/image.png)


![](https://images.velog.io/images/earthkingman/post/c979a516-f69e-4604-a0a2-af69a8b14114/image.png)

- 결론

![](https://images.velog.io/images/earthkingman/post/56d9fd71-944a-4dce-8e41-6fba83742203/image.png)

위와 같이 600원이라는 오차가 생겼습니다. 요청을 직렬화 하지는 못했지만 클라이언트에게 출금 입금 실패를 응답하게 했습니다.

기존과 달라진 부분은 데이터베이스에 락이 걸려 요청이 실패된다면 클라이언트가 알 수 있게 되었습니다.



#### 방법 3. 데이터 베이스를 변경

기존의 코드와 환경은 동일합니다. 

sqlite는 `select_for_update`을 지원하지 않는다는 정보를 알게되었고, mysql로 데이터베이스를 변경해보았습니다.

계좌번호1에 기본금 1000원이 있습니다.

입금 출금을 동시에 100원씩 1000번  진행했고, 에러메세지는 발생하지 않았습니다.

![image-20220115142724001](/Users/ji-park/Library/Application Support/typora-user-images/image-20220115142724001.png)



- 결과

  문제 목표와 같이 동시 접근을 막고 하나의 트랜잭션만 작동합니다. 그리고 나머지는 순차적으로 대기합니다.

  거래내역의 잔액과 계좌의 잔액은 오차가 생기지 않고 정확합니다.

  - 거래내역

    <img src="https://images.velog.io/images/earthkingman/post/3e82dc9a-40ce-4453-9e9b-34bca1c5ff7d/image.png" width="500px">

  - 잔액

<img src="https://images.velog.io/images/earthkingman/post/ee8fa856-d79b-45e2-8d6b-99501c0ad229/image.png" width="500px">



#### 방법 4. Mysql을 사용하고 락을 사용하지 않고 격리수준을 변경해보기

10000원에 100원씩 입출금을 동시에 여러번 진행했습니다.

- REPEATABLE-READ

  ![](https://images.velog.io/images/earthkingman/post/54923a6f-c0cf-47af-ad38-6bce8a0944ac/image.png)

- SERIALIZABLE

  - 격리 수준 확인과 변경 방법

  ```sql
  SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE
  
  SELECT @@SESSION.transaction_isolation
  ```

  ![](https://images.velog.io/images/earthkingman/post/e2cbcfa2-b146-4dbc-b141-401188885447/image.png)

동시에 접근해 읽는 경우가 생겨 오차가 생겼습니다.

![](https://images.velog.io/images/earthkingman/post/3eeeebd1-6a61-4bec-8cba-1df1dcec6f2d/image.png)

- 의문점

  데이터베이스의 격리수준은 아무런 효과가 없는것인가??



---

#### 거래내역이 1억건을 넘어서는 경우 어떻게하면 조회를 빨리 할 수 있을까?

- 문제

  거래내역 1억건이 넘어서면 수 많은 문제들이 생깁니다. 수 많은 문제 중 조회에 초점을 두었습니다.

  조회는 거래내역이 1억건을 넘어선다면 속도가 매우 느려집니다.

- 목표

  인덱스를 생성해서 조회 속도를 개선해야합니다. 인덱스의 구조를 파악하고, 왜 빨라지는지 어떻게 빨라지는지 확인합니다.

- 해결

  테이블을 생성해보겠습니다.

  - Account(계좌), Users(사용자), Transaction(거래내역) 테이블 생성

    sqlite는  기본 키(primary key)나 유일 키(unique) 제약 조건을 지정하면 자동으로 인덱스가 생성됩니다. 

    그래서 Datagrip으로 생성된 인덱스들을 확인 했습니다.

    - Account 테이블에서는 account_number(유니크 키), user_id (외래키),  

    - Transaction 테이블에서는 account_id(외래키)

    - User 테이블에서는 email(유니크키)

    생성해서 얻는 이득은 참조 키를 빠르게 확인하고 테이블 스캔을 하지 않을 수 있습니다.

    

  ![](https://images.velog.io/images/earthkingman/post/88577f81-040a-45f2-a477-8bc0ab051a80/image.png)

  

  ![](https://images.velog.io/images/earthkingman/post/ba91e1d6-1253-43b9-a412-d3012492fe69/image.png)

  서버에서 실제로 호출하는 Query 입니다. 

  실행계획을 통해 이 쿼리들이 인덱스를 타는지 확인해보았습니다.

  - 조회하기 

    ```sql
    SELECT * FROM "transaction_transaction" 
    WHERE "transaction_transaction"."account_id" = 1 
    ORDER BY "transaction_transaction"."id" ASC LIMIT 10
    ```

    ![](https://images.velog.io/images/earthkingman/post/c928772c-f97e-443f-91c8-7565b73aa6c8/image.png)

  - 날짜로 조회하기 

    ```sql
    SELECT *
    WHERE ("transaction_transaction"."account_id" = 1
    AND "transaction_transaction"."created_at" >= '2022-01-10 00:00:00' 
    AND "transaction_transaction"."created_at" <= '2022-01-12 00:00:00' ) 
    ORDER BY "transaction_transaction"."id" ASC LIMIT 10
    ```

    ![](https://images.velog.io/images/earthkingman/post/5a59ec80-6611-4c62-bdf4-2b2f8e3d0107/image.png)

  - 입출금 구분으로 조회하기  

    ```sqlite
    SELECT * FROM "transaction_transaction" 
    WHERE ("transaction_transaction"."account_id" = 1
    AND "transaction_transaction"."transaction_type" = 출금)
    ORDER BY "transaction_transaction"."id" ASC LIMIT 10
    ```

    ![](https://images.velog.io/images/earthkingman/post/607957d6-b8ea-4423-b628-592782f58c59/image.png)

    

  - 결과(데이터 약 100만개)

    | 검색 조건        | 자동으로 생성된 인덱스 사용    | 자동으로 생성된 인덱스 지워보기 |
    | ---------------- | ------------------------------ | ------------------------------- |
    | 기본             | 66ms (인덱스 탔음 account_id)  | 103ms (인덱스 안탐)             |
    | 날짜로 검색      | 426ms (인덱스 탔음 account_id) | 399ms  (인덱스 안탐)            |
    | 입출금 검색      | 254ms (인덱스 탔음 account_id) | 231ms  (인덱스 안탐)            |
    | 날짜 입출금 검색 | 560ms (인덱스 탔음 account_id) | 526ms  (인덱스 안탐)            |

    단일 인덱스로는 해당 데이터에 바로 접근을 하지 못하는 경우들은 오히려 인덱스가 없는게 더 빨랐습니다.

    

  - 기본 검색은 왜 빨라진걸까?

    단일 인덱스 (account_id)로 바로 데이터에 접근할 수 있기 때문입니다.

    그리고 인덱스 테이블은 항상 정렬되어 있습니다. 

    ![](https://images.velog.io/images/earthkingman/post/11c6c55e-be1f-482e-aeca-e3eb02a72f7b/image.png)

    

  - 그럼 다른 검색들은 왜 인덱스를 사용했는데 속도가 느려지는걸까?

    이유는 단일 컬럼을 사용하는 경우에는 여러개의 컬럼을 Where절에서 사용한다면  데이터가 바로 접근하지 못합니다. 

    결국 여러번 디스크에 엑세스를 해야하는 문제가 생깁니다. 

    

  - 인덱스를 타는 기준이 뭘까? 

    Where 조건에 인덱스 컬럼이 있다면  인덱스를 타게 됩니다.

    

  - 여러개의 인덱스 중 어떤 것을 선정하고 어떤 기준으로 선정하는걸까?

    단일컬럼으로 테스트한 결과입니다

    | 검색 조건        | 단일컬럼 인덱스3개  (create_ad),(account_id), (transaction) |
    | ---------------- | ----------------------------------------------------------- |
    | 기본             | 66ms (account_id 인덱스 탔음)                               |
    | 날짜로 검색      | 426ms (account_id 인덱스 탔음)                              |
    | 입출금 검색      | 254ms (account_id 인덱스 탔음)                              |
    | 날짜 입출금 검색 | 558ms  (account_id인덱스 탔음)                              |

    단일컬럼 인덱스가 있는 경우에는 where절의 가장 앞에 있는 조건을 우선으로 인덱스를 정한다는 추측을 하였으나

    테스트를 진행해보니 틀렸었습니다.  

    옵티마이저가 최적의 엑세스 경로를 찾아준다고 하는데 힌트를 사용하면 사용자가 직접 최적의 튜닝이 가능합니다.

    

  - 그럼 내 서비스는 어떻게 해야 조회속도를 높힐 수 있을까?

    **멀티컬럼 인덱스 사용**

    인덱스는 하나의 컬럼으로 작성할 수도 있고, 여러개의 컬럼을 사용해서 멀티 컬럼 인덱스를 만들 수도 있습니다.

    제 서비스는(계좌번호, 날짜), (계좌번호, 입출금) 등등  다중 조건으로 조회하기 때문에

    이러한 칼럼을 모두 포함하는  멀티 컬럼 인덱스가 적합합니다. 

    

  - 멀티컬럼 인덱스를 생성하는 기준

    중복된 수치를 나타내는 카디널리티가 가장 높은것을 선택해야합니다. 이유는 해당 인덱스로 많은 부분을 걸러내야 하기 때문입니다.

    중복된 수치가 높으면 카디널리티가 낮고 중복된 수치가 낮으면 카디널리티가 높습니다.

    하지만 주의해야할 것이있습니다. 카디널리티는 높은순에서 낮은순으로 나열해야 합니다.

    

  - 왜  카디널리티는 높은순에서 낮은순으로 나열해야하는 걸까?

    인덱스를 걸 때, 내가 원하는 데이터를 선택하는 과정에서 최대한 많은 데이터가 걸러져야 성능이 좋을 것 입니다.

    중복적인 데이터가 많은 transaction_type 인덱스가첫 번째로 오는 경우에는 비교적 데이터를 걸러내지 못합니다.

    ```sql
    select * from transaction
    where account_id = 3
    AND   transaction_type = '출금'
    ```

    - `transaction_type,account_id`

    ![](https://images.velog.io/images/earthkingman/post/4dae7836-a187-413c-9384-41b24e95ffa4/image.png)

    

    - `account_id, transaction_type`

    ![](https://images.velog.io/images/earthkingman/post/f0edaa56-6dcf-49e3-9ad1-baea26e4dbe5/image.png)

    

  - 내 서비스에 적용시켜 보기

  - - 카디널리티가 높은순에서 낮은순  `created_at, account_id, transaction_type`

    ```python
     class Meta:
            db_table = 'transaction_history'
            indexes = [
                models.Index(
                    fields=['created_at', 'account_id', 'transaction_type']),
            ]
    ```

    

    - 카디널리티가 낮은순에서 높은순 `transaction_type, account_id, created_at, `

    ```python
     class Meta:
            db_table = 'transaction_history'
            indexes = [
                models.Index(
                    fields=['transaction_type', 'account_id', 'created_at']),
            ]
    ```

    - 결과(데이터 약 100만개)

      조회 쿼리 사용시 인덱스를 태우려면 최소한 **첫번째 인덱스 조건은 조회조건에 포함**되어야만 합니다.

      | 검색 조건        | 높은순에서 낮은순 (날짜->계좌->종류)            | 낮은순에서 높은순 (종류->계좌->날짜)            |
      | ---------------- | ----------------------------------------------- | ----------------------------------------------- |
      | 기본             | 92ms(인덱스 안탐)                               | 93ms  (인덱스 안탐)                             |
      | 날짜로 검색      | 239ms  (인덱스 탐) USE TEMP B-TREE FOR ORDER BY | 402ms (인덱스 안탐)                             |
      | 입출금 검색      | 220ms (인덱스 안탐)                             | 135ms  (인덱스 탐) USE TEMP B-TREE FOR ORDER BY |
      | 날짜 입출금 검색 | 478ms (인덱스 탐) USE TEMP B-TREE FOR ORDER BY  | 150ms  (인덱스 탐) USE TEMP B-TREE FOR ORDER BY |

      - 이론적으로는 높은순에서 낮은순이 속도가 더 빨라야하는데 날짜 입출금 검색은 결과가 반대일까?

        날짜 인덱스로 가장 먼저 정렬을 하기 때문에 계좌 인덱스와 종류 인덱스는 인덱스 적용이 되지 않습니다. 

        이유는 `between`, `like`, `<`, `>` 등 범위 조건 해당 컬럼은 인덱스를 타지만, 그 뒤 인덱스 컬럼들은 인덱스가 사용되지 않기 때문입니다.

        그래서 날짜 인덱스로만 데이터에 접근할 수 없고, 낮은순에서 높은순 보다 속도가 느려진것입니다.

      

      ![](https://images.velog.io/images/earthkingman/post/cc491452-735c-4ed3-a5f0-fe3a55544945/image.png)

      

      USE TEMP B-TREE FOR ORDER BY의 의미를 파악하지 못했습니다.

    

    - 결론

      제 서비스에 적합하게 인덱스를 걸어줘야합니다.

      ```python
      class Transaction(models.Model):
          account = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
          balance = models.PositiveBigIntegerField(null=False, validators=[validate_balance])
          amount = models.PositiveBigIntegerField(null=False, validators=[validate_amount])
          t_type = models.CharField(max_length=2, null=False,validators=[validate_type])
          description = models.CharField(max_length=50, null=False)
          created_at = models.DateTimeField(auto_now_add=True)
      
          class Meta:
              db_table = 'transaction_index'
              indexes = [
                  models.Index(fields=['account_id', 'transaction_type','created_at']),#index1
                  models.Index(fields=['account_id', 'transaction_type']), #index2
                  models.Index(fields=['account_id', 'created_at']), #index3
                  models.Index(fields=['account_id']) #index4 
              ]
      
      ```

      - **데이터 약 백만 개**

      | 검색 조건        | 인덱싱         |
      | ---------------- | -------------- |
      | 기본             | 84ms (index4)  |
      | 날짜로 검색      | 189ms (index3) |
      | 입출금 검색      | 58ms (index2)  |
      | 날짜 입출금 검색 | 153ms (index1) |

      

  

### 12. 테스트

#### 코드 커버리지 98%

총 45개의 테스트 코드를 작성했고 코드 커버리지는 98%입니다.

 <img src = "https://user-images.githubusercontent.com/48669085/148824915-d2b1adff-1db5-4043-a9af-79b18c640201.png" width="800px">
