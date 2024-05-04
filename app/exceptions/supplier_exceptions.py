from app.exceptions import BaseExceptions


class SupplierNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Supplier not found"


class SupplierBadParameters(BaseExceptions):
    status_code: int = 400
    detail: str = "Invalid parameters passed"
