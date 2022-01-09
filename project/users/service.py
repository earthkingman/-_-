from users.models import User
import bcrypt
from users.utils import accessSign


class UserDuplicateError(Exception):  # 유저 중복
    pass


class UserNotExistError(Exception):  # 존재하지 않는 유저
    pass


class PasswordInvalid(Exception):  # 유효하지 않은 비밀번호
    pass


class UserService:
    def signup(self, email: str, password: str):
        hash_password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        if User.objects.filter(email=email).exists():
            raise UserDuplicateError

        User.objects.create(
            email=email,
            password=hash_password
        )

    def login(self, email: str, password: str):
        user = User.objects.filter(email=email)

        if not user.exists():
            raise UserNotExistError

        # 원리 파악하기
        if bcrypt.checkpw(password.encode('utf-8'), user[0].password.encode('utf-8')):
            access_token = accessSign(user)
            return access_token
        else:
            raise PasswordInvalid
