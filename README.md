# 8퍼센트
### 1. 과제 안내
📝 다음과 같은 내용을 포함하는 테이블을 설계하고 다음과 같은 기능을 제공하는 REST API 서버를 개발해주세요.
1. REST API 기능

    - 거래내역 조회 API
    - 입금 API
    - 출금 API

2. 개발 조건
2-1. 고려사항

    - 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
    - DB를 설계 할때 각 칼럼의 타입과 제약
    
### 2. 개발 환경

    - python 3.9.1
    - django 4.0
    - sqlite
    
### 3. 프로젝트 구조


### 4. 디렉토리 구조

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
    
### 4. API 명세


### 5. 빌드 및 실행 방법



