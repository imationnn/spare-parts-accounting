from pydantic import BaseModel, Field
from datetime import datetime

from app.models.base import num_20_2
from app.schemas import SupplierListOut


class Employee(BaseModel):
    id: int
    full_name: str


class Supplier(SupplierListOut):
    pass


class NewArrivalIn(BaseModel):
    invoice_number: str = Field(min_length=2, max_length=30)
    invoice_date: str
    supplier_id: int
    total_price: num_20_2


class NewArrivalOut(NewArrivalIn):
    id: int
    created_at: datetime
    shop_id: int
    is_transferred: bool
    employee: Employee
    supplier: Supplier
