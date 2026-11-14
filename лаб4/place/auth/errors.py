class JWTError(Exception):
    pass


class TokenExpiredError(JWTError):
    pass


class TokenVerificationError(JWTError):
    pass
