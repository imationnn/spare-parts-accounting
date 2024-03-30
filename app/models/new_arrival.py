from sqlalchemy import ForeignKey
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, def_false


class NewArrival(Base):
    invoice_number: Mapped[str] = mapped_column(unique=True)
    invoice_data: Mapped[str]
    created_at: Mapped[created_at]
    shop_id: Mapped[int]
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    total_price: Mapped[Decimal] = mapped_column(default=0, server_default="0")
    is_transferred: Mapped[def_false]


class NewArrivalDetail(Base):
    part_id: Mapped[int]
    created_at: Mapped[created_at]
    qty: Mapped[int]
    price_in: Mapped[Decimal]
    price_out: Mapped[Decimal]
    amount: Mapped[Decimal]
    currency: Mapped[str] = mapped_column(default="RUB", server_default="RUB")
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    ccd: Mapped[str | None]
    arrive_id: Mapped[int] = mapped_column(ForeignKey("new_arrivals.id"))
