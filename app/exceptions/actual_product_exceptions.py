from app.exceptions import BaseExceptions


class ProductNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Actual product not found"


class ProductDateRangeExceeded(BaseExceptions):
    status_code: int = 400

    def __init__(self, date_range: int | str):
        self.detail = f"Date range exceeded, available limit {date_range} days"


class ProductBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters passed"
