from app.exceptions import BaseExceptions


class InvalidLoginPass(BaseExceptions):
    status_code: int = 401
    detail: str = "Invalid login or password"


class AccessIsDenied(BaseExceptions):
    status_code: int = 403
    detail: str = "Access is denied"


class InvalidToken(BaseExceptions):
    status_code: int = 401
    detail: str = "Invalid token"


class InvalidTokenType(BaseExceptions):
    status_code: int = 401
    detail: str = "Invalid token type"
