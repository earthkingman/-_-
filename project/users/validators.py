from django.core.exceptions import ValidationError


def validate_email(email: str) -> str:
    try:
        if len(email) < 3 or len(email) > 50:
            msg = "이메일 길이는 3보다 크고 20보다 작아야 합니다"
            raise ValidationError(msg)
        return email

    except (TypeError, ValueError, KeyError):
        msg = "이메일은 문자를 넣어주세요"
        raise ValidationError(msg)


def validate_password(password: str) -> str:
    try:
        if len(password) < 3 or len(password) > 20:
            msg = "비밀번호 길이는 3보다 크고 20보다 작아야 합니다"
            raise ValidationError(msg)
        return password

    except (TypeError, ValueError, KeyError):
        msg = "비밀번호는 문자를 넣어주세요"
        raise ValidationError(msg)
