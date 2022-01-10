from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from transaction.constant import DEPOSIT, WITHDRAW


# 잔액 검증(모델)
def validate_balance(balance: int):
    if (balance < 0):
        msg = "잔액은 음수가 될 수 없습니다."
        raise ValidationError(msg)


# 거래 종류 검증(모델)
def validate_t_type(transaction_type: str) -> str:
    if (transaction_type != WITHDRAW and transaction_type != DEPOSIT):
        msg = "거래는 출금과 입금만 가능합니다."
        raise ValidationError(msg)

    return transaction_type


# 금액 검증
def validate_amount(amount: int) -> int:
    try:
        amount = int(amount)
    except (TypeError, ValueError, KeyError):
        msg = "정수를 넣어주세요"
        raise ValidationError(msg)
    if amount <= 0:
        msg = "0보다 같거나 작은 금액은 거래할 수 없습니다."
        raise ValidationError(msg)
    return amount


# 적요 검증
def validate_description(description: str) -> str:
    description = str(description)

    if len(description) < 1 or len(description) > 20:
        msg = "적요 길이는 0보다 크고 20보다 작아야 합니다"
        raise ValidationError(msg)
    return description


# 계좌번호 검증
def validate_account_number(account_number: str) -> str:
    account_number: str = str(account_number)

    if len(account_number) < 3 or len(account_number) > 20:
        msg = "계좌번호 길이는 2보다 크고 20보다 작아야 합니다"
        raise ValidationError(msg)
    return account_number


# 시작 날짜 검증
def validate_start_date(start_at: str) -> datetime:
    try:
        if start_at is None:
            return None
        start_date: datetime = datetime.strptime(start_at, '%Y-%m-%d')
        return start_date
    except (TypeError, ValueError, KeyError):
        msg: str = "날짜 형식이 아닙니다."
        raise ValidationError(msg)


# 종료 날짜 검증
def validate_end_date(end_at: str) -> datetime:
    try:
        if end_at is None:
            return None
        end_date: datetime = datetime.strptime(end_at, '%Y-%m-%d')
        end_date: datetime = end_date + timedelta(days=1)
        return end_date
    except (TypeError, ValueError, KeyError):
        msg: str = "날짜 형식이 아닙니다."
        raise ValidationError(msg)


# 거래 내역 출입금 종류 검증
def validate_list_t_type(transaction_type: str) -> str:
    if (transaction_type != WITHDRAW and transaction_type != DEPOSIT and transaction_type is not None):
        msg: str = "거래는 출금과 입금, 기본만 가능합니다."
        raise ValidationError(msg)
    return transaction_type
