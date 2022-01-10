
class UserDuplicateError(Exception):  # 유저 중복
    pass


class UserNotExistError(Exception):  # 존재하지 않는 유저
    pass


class PasswordInvalidError(Exception):  # 유효하지 않은 비밀번호
    pass
