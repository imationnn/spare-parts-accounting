from app.exceptions import BaseExceptions


class BrandNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Нет такого бренда"


class BrandAlreadyExist(BaseExceptions):
    status_code: int = 409
    detail: str = "Такой бренд уже есть"
