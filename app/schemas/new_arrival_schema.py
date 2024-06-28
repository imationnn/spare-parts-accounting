from pydantic import Field
from datetime import datetime

from app.models.base import num_20_2
from app.schemas import SupplierListOut, CatalogOutByNumber, BaseSchema


class Employee(BaseSchema):
    id: int
    full_name: str


class Supplier(SupplierListOut):
    pass


class NewArrivalIn(BaseSchema):
    invoice_number: str = Field(min_length=2, max_length=30)
    invoice_date: str = Field(examples=["15.01.2024"])
    supplier_id: int
    total_price: num_20_2 = Field(default=0, ge=0)


class ArrivalNewOut(NewArrivalIn):
    id: int
    created_at: datetime
    shop_id: int
    is_transferred: bool


class NewArrivalOut(ArrivalNewOut):
    employee: Employee
    supplier: Supplier


class ArrivalDetailNewIn(BaseSchema):
    part_id: int
    qty: int = Field(gt=0)
    amount: num_20_2 = Field(ge=0)
    ccd: str | None = None
    arrive_id: int


class ArrivalDetailNewOut(ArrivalDetailNewIn):
    id: int
    created_at: datetime
    price_in: num_20_2
    currency: str
    employee_id: int


class NewArrivalDetailGetList(ArrivalDetailNewOut):
    part: CatalogOutByNumber
    employee: Employee


class NewArrivalUpdateIn(BaseSchema):
    invoice_number: str | None = Field(default=None, min_length=2, max_length=30)
    invoice_date: str | None = Field(default=None, examples=["15.01.2024"])
    supplier_id: int | None = None
    total_price: num_20_2 | None = Field(default=None, ge=0)


class NewArrivalUpdateOut(ArrivalNewOut):
    employee_id: int


class NewArrivalDetailUpdateIn(BaseSchema):
    part_id: int | None = None
    qty: int | None = Field(default=None, gt=0)
    amount: num_20_2 | None = Field(default=None, ge=0)
    ccd: str | None = None


class NewArrivalDetailUpdateOut(ArrivalDetailNewOut):
    pass


class NewArrivalDeleteOut(ArrivalNewOut):
    pass


class NewArrivalDetailDeleteOut(ArrivalDetailNewOut):
    pass
