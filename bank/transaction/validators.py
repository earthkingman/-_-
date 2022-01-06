from django.core.exceptions import ValidationError


# def validate_amount(value):
#     if (value <= 0):
#         msg = "0보다 같거나 작은 금액은 거래할 수 없습니다."
#         raise ValidationError(msg)


# def validate_type(value):
#     if (value != "출금" and value != "입금"):
#         msg = "거래는 출금과 입금만 가능합니다."
#         raise ValidationError(msg)


def validate_balance(value):
    if (value < 0):
        msg = "잔액은 음수가 될 수 없습니다."
        raise ValidationError(msg)


def validate_t_type(t_type: str):
    if (t_type != "출금" and t_type != "입금"):
        msg = "거래는 출금과 입금만 가능합니다."
        raise ValidationError(msg)
    return t_type


def validate_amount(amount: int):
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        msg = "정수를 넣어주세요"
        raise ValidationError(msg)
    if amount <= 0:
        msg = "0보다 같거나 작은 금액은 거래할 수 없습니다."
        raise ValidationError(msg)
    return amount


def validate_description(description: str):
    try:
        description = str(description)
        msg = "적요를 제대로 적어주세요"
    except (TypeError, ValueError):
        raise ValidationError(msg)
    return description


def validate_account_number(account_number: str):
    try:
        account_number = str(account_number)
        msg = "계좌번호를 제대로 적어주세요"
    except (TypeError, ValueError):
        raise ValidationError(msg)
    return account_number
