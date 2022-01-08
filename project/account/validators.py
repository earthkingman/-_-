from django.core.exceptions import ValidationError


def validate_balance(value):
    if (value < 0):
        msg = "잔액은 음수가 될 수 없습니다."
        raise ValidationError(msg)
