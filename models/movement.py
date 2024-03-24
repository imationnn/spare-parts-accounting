from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, int_def0


class Movement(Base):
    from_shop_id: Mapped[int]
    to_shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    created_at: Mapped[created_at]
    arrived_at: Mapped[datetime | None]
    created_employee_id: Mapped[int]
    accepted_employee_id: Mapped[int | None]
    total_price: Mapped[int_def0]
    is_sent: Mapped[bool] = mapped_column(default=False, server_default="False")
    is_deleted: Mapped[bool] = mapped_column(default=False, server_default="False")


class MovementDetail(Base):
    product_id: Mapped[int]
    status: Mapped[int]
    qty: Mapped[int]
    price: Mapped[int]
    amount: Mapped[int]
    created_at: Mapped[created_at]
    move_id: Mapped[int]
    employee_id: Mapped[int]
    is_deleted: Mapped[bool]
