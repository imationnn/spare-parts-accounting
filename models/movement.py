from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, int_def0, def_false


class StatusMovements:  # TODO добавить статусы
    pass


class Movement(Base):
    from_shop_id: Mapped[int]
    to_shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    created_at: Mapped[created_at]
    arrived_at: Mapped[datetime | None]
    created_employee_id: Mapped[int]
    accepted_employee_id: Mapped[int | None]
    total_price: Mapped[int_def0]
    is_sent: Mapped[def_false]
    is_deleted: Mapped[def_false]


class MovementDetail(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("actual_products.id"))
    status: Mapped[int]  # TODO добавить дефолтный статус
    qty: Mapped[int]
    amount: Mapped[int]
    created_at: Mapped[created_at]
    move_id: Mapped[int] = mapped_column(ForeignKey("movements.id"))
    employee_id: Mapped[int]
    is_deleted: Mapped[def_false]


class StatusMovement(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
