from app.exceptions import BaseExceptions


class ShopNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Shop not found"


class ShopBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters or existing shop name or ip address passed"
