from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at, def_false, num_20_2


if TYPE_CHECKING:
    from app.models import Employee, Supplier


class NewArrival(Base):
    invoice_number: Mapped[str] = mapped_column(unique=True)
    invoice_date: Mapped[str]
    created_at: Mapped[created_at]
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    total_price: Mapped[num_20_2] = mapped_column(default=0, server_default="0")
    is_transferred: Mapped[def_false]

    employee: Mapped["Employee"] = relationship()
    supplier: Mapped["Supplier"] = relationship()


class NewArrivalDetail(Base):
    part_id: Mapped[int]
    created_at: Mapped[created_at]
    qty: Mapped[int]
    price_in: Mapped[num_20_2]
    price_out: Mapped[num_20_2]
    amount: Mapped[num_20_2]
    currency: Mapped[str] = mapped_column(default="RUB", server_default="RUB")
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    ccd: Mapped[str | None]
    arrive_id: Mapped[int] = mapped_column(ForeignKey("new_arrivals.id"))
