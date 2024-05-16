from app.exceptions import BaseExceptions


class ArrivalNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Arrival does not exist"


class ArrivalDateRangeExceeded(BaseExceptions):
    status_code: int = 400

    def __init__(self, date_range: int | str):
        self.detail = f"Date range exceeded, available limit {date_range} days"


class ArrivalAlreadyExist(BaseExceptions):
    status_code: int = 409
    detail: str = "Arrival already exist, check invoice number or supplier id"


class ArrivalBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters passed"


class ArrivalAlreadyTransferred(BaseExceptions):
    status_code: int = 400
    detail: str = "Arrival already transferred"


class ArrivalCheckAmount(BaseExceptions):
    status_code: int = 400
    detail: str = "Check the amount"


class ArrivalNothingTransfer(BaseExceptions):
    status_code: int = 400
    detail: str = "Nothing to transfer"
