from users.models import User
import bcrypt  # SHA-2
from users.utils import accessSign
from users.error import UserDuplicateError, PasswordInvalidError, UserNotExistError


class UserService:
    def signup(self, email: str, password: str):

        if User.objects.filter(email=email).exists():
            raise UserDuplicateError

        salt: bytes = bcrypt.gensalt()
        encoded_password: bytes = password.encode("utf-8")
        hashed_password: bytes = bcrypt.hashpw(encoded_password, salt)
        decoded_password: str = hashed_password.decode("utf-8")

        User.objects.create(
            email=email,
            password=decoded_password
        )

    def login(self, email: str, password: str):
        user = User.objects.filter(email=email)

        if not user.exists():
            raise UserNotExistError

        if bcrypt.checkpw(password.encode('utf-8'), user[0].password.encode('utf-8')):
            access_token: bytes = accessSign(user)
            return access_token
        else:
            raise PasswordInvalidError
