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


### 7. API 명세 및 설명

### 8. 사전과제가 요구한 것
![image](https://user-images.githubusercontent.com/48669085/148150818-fd921844-42cc-428c-a2fc-c2d644cc55f2.png)


### 9. 개발 과정에서 해결한 문제들

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


