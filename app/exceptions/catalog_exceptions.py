from app.exceptions import BaseExceptions


class PartNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Part number not found"


class PartBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters or existing part number passed"
