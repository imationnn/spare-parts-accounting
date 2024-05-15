from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime

from app.models.base import num_20_2
from app.schemas import SupplierListOut, CatalogOutByNumber


class Employee(BaseModel):
    id: int
    full_name: str


class Supplier(SupplierListOut):
    pass


class Part(BaseModel):
    part_id: int
    margin_value: Decimal = Field(ge=1, decimal_places=2)


class NewArrivalIn(BaseModel):
    invoice_number: str = Field(min_length=2, max_length=30)
    invoice_date: str = Field(examples=["15.01.2024"])
    supplier_id: int
    total_price: num_20_2 = Field(default=0)


class ArrivalNewOut(NewArrivalIn):
    id: int
    created_at: datetime
    shop_id: int
    is_transferred: bool


class NewArrivalOut(ArrivalNewOut):
    employee: Employee
    supplier: Supplier


class NewArrivalDetail(BaseModel):
    qty: int = Field(gt=0)
    amount: num_20_2
    ccd: str | None = None
    arrive_id: int


class ArrivalDetailNewIn(NewArrivalDetail):
    part: Part


class ArrivalDetailNewOut(NewArrivalDetail):
    id: int
    part_id: int
    created_at: datetime
    price_in: num_20_2
    currency: str
    employee_id: int


class NewArrivalDetailGetList(ArrivalDetailNewOut):
    part: CatalogOutByNumber
    employee: Employee


class NewArrivalUpdateIn(BaseModel):
    invoice_number: str | None = Field(default=None, min_length=2, max_length=30)
    invoice_date: str | None = Field(default=None, examples=["15.01.2024"])
    supplier_id: int | None = None
    total_price: num_20_2 | None = None


class NewArrivalUpdateOut(ArrivalNewOut):
    employee_id: int


class NewArrivalDetailUpdateIn(BaseModel):
    part_id: int | None = None
    qty: int | None = Field(default=None, gt=0)
    amount: num_20_2 | None = None
    ccd: str | None = None


class NewArrivalDetailUpdateOut(ArrivalDetailNewOut):
    pass


class NewArrivalDeleteOut(ArrivalNewOut):
    pass


class NewArrivalDetailDeleteOut(ArrivalDetailNewOut):
    pass
