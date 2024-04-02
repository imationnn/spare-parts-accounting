from app.exceptions import BaseExceptions


class PartNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Деталь не найдена"


class PartBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Переданы неверные параметры или существующий номер детали"
