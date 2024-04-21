from app.exceptions import BaseExceptions


class BrandNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Brand not found"


class BrandAlreadyExist(BaseExceptions):
    status_code: int = 409
    detail: str = "Brand already exist"


class BrandCannotBeDeleted(BaseExceptions):
    status_code: int = 409
    detail: str = "Brand cannot be deleted"
