from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime

from app.models.base import num_20_2
from app.schemas import SupplierListOut


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
    qty: int
    amount: num_20_2
    ccd: str | None = None
    arrive_id: int


class NewArrivalDetailIn(NewArrivalDetail):
    part: Part


class NewArrivalDetailOut(NewArrivalDetail):
    id: int
    part_id: int
    created_at: datetime
    price_in: num_20_2
    price_out: num_20_2
    currency: str
    employee_id: int
