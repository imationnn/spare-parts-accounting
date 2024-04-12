from app.exceptions import BaseExceptions


class EmployeeNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Employee not found"


class EmployeeAlreadyExist(BaseExceptions):
    status_code: int = 409
    detail: str = "Employee already exist"


class EmployeeBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters or existing employee id passed"
