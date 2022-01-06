from django.core.exceptions import ValidationError


def validate_amount(value):
    if (value <= 0):
        msg = "0보다 같거나 작은 금액은 거래할 수 없습니다."
        raise ValidationError(msg)


def validate_balance(value):
    if (value < 0):
        msg = "잔액은 음수가 될 수 없습니다."
        raise ValidationError(msg)


def validate_type(value):
    if (value != "출금" and value != "입금"):
        msg = "거래는 출금과 입금만 가능합니다."
        raise ValidationError(msg)
