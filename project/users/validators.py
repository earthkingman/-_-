from django.core.exceptions import ValidationError


def validate_email(email: str) -> str:
    email: str = str(email)
    if len(email) < 3 or len(email) > 50:
        msg = "이메일 길이는 3보다 크고 20보다 작아야 합니다"
        raise ValidationError(msg)
    return email


def validate_password(password: str) -> str:
    password: str = str(password)
    if len(password) < 3 or len(password) > 20:
        msg = "비밀번호 길이는 3보다 크고 20보다 작아야 합니다"
        raise ValidationError(msg)
    return password
