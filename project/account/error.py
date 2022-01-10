
class ExitsError(Exception):  # 계좌 존재 X
    pass


class AccountAuthError(Exception):  # 계좌 권한
    pass


class AccountDuplicateError(Exception):  # 계좌 중복
    pass
