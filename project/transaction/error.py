
class ExitsError(Exception):  # 계좌 존재 X
    pass


class AccountAuthError(Exception):  # 계좌 권한
    pass


class BalanceError(Exception):  # 잔액 부족
    pass


class LockError(Exception):  # 서버 오류(락 걸렸을떄)
    pass
