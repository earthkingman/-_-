### 1. 과제 안내

1. REST API 기능

   - 거래내역 조회 API
   - 입금 API
   - 출금 API

2. Localhost에서 돌리는 방법

   Python 3.~ 부터 가능합니다.

   - 프로젝트 설치

     ```shell
     $ git clone https://github.com/earthkingman/8Percent
     ```

   - 가상환경 생성 및 접속 및 모듈 설치

     ```shell
     $ virtualenv 8percent
     $ source bin/activate
     
     ## ~/8Percent/project
     pip install -r requirements.txt
     ```

   - 설정 파일 생성

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

### 2. 문제 정의

- 문제 

  계좌의 잔액을 별도로 관리할 수 있고, 계좌의 잔액과 거래내역의 잔액의 무결성을 보장할 수 있어야 합니다.

- 해결 목표

  사용자는 계좌를 생성할 수 있고, 자기의 계좌에만 입출금이 가능하며 거래내역을 생성하고 조회할 수 있는 프로그램 제작

### 3. 문제별 해결 방법

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



### 4. 구현 사항

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

### 



### 5. 개발 환경 및 프로젝트 구조

<img src = "https://user-images.githubusercontent.com/48669085/148770760-b9ab6029-9005-4661-b0e6-6b31471d3c69.png" width="650px">

```
- python 3.9.1
- django 4.0
- sqlite 3.0
```

### 6. ER-D

![image](https://images.velog.io/images/earthkingman/post/d519d304-8cfe-40fd-8ae9-9c3c1418d336/image.png)

### 7. 디렉토리 구조

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



### 8. 서비스 구조



<img src="https://images.velog.io/images/earthkingman/post/b95d1307-1d42-49e4-9dbb-07ae0d6cf51d/image.png" height="800px" width="800px">



### 9. API 명세 및 설명









### 10. 도전했지만 완벽하게 해결하지 못한 부분

#### 거래내역이 1억건을 넘어서는 경우 어떻게하면 조회를 빨리 할 수 있을까?

- 문제

  거래내역 1억건이 넘어서면 수 많은 문제들이 생깁니다. 수 많은 문제 중 조회에 초점을 두었습니다.

  조회는 거래내역이 1억건을 넘어선다면 속도가 매우 느려집니다.

- 목표

  조회 속도를 개선해야합니다.

- 해결

  멀티 컬럼 인덱스를 생성했습니다.

  인덱싱을 생성하니 조회가 조금 개선되었습니다.

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



#### 동시성 문제 해결

- 문제

  잔액에 동시에 접근했을 때 금액 오류가 발생합니다.

- 목표

  트랜잭션을 직렬화 해서 동시성 문제를 해결합니다.

  ![](https://images.velog.io/images/earthkingman/post/92383ca7-2236-4471-a24f-14946fe1916f/image.png)

  #### 도전

​		계좌 1004번은 10000원을 가지고 있습니다.

- 출금 코드 

```python
    # 출금 (트랜잭션)
    @transaction.atomic
    def withdraw(self, account, amount, description):
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

```shell
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

#### select_for_update을 사용해 락을 거는 방법

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



#### 결과

![](https://images.velog.io/images/earthkingman/post/56d9fd71-944a-4dce-8e41-6fba83742203/image.png)

위와 같이 600원이라는 오차가 생겼습니다. 요청을 직렬화 하지는 못했지만 클라이언트에게 출금 입금 실패를 응답하게 했습니다.

기존과 달라진 부분은 데이터베이스에 락이 걸려 요청이 실패된다면 클라이언트가 알 수 있게 되었습니다.



### 11. 테스트

#### 코드 커버리지 98%

총 45개의 테스트 코드를 작성했고 코드 커버리지는 98%입니다.

![](https://images.velog.io/images/earthkingman/post/e31afc6b-13c6-4852-a4e2-be0b79b7e2b8/image.png)



