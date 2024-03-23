from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, int_def0


class ActualProduct(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("catalog_parts.id"))
    arrived: Mapped[int]
    released: Mapped[int_def0]
    rest: Mapped[int]
    price: Mapped[int]
    movement_id: Mapped[int | None]
    reserve: Mapped[int_def0]
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    arrive_id: Mapped[int]
    arrived_at: Mapped[created_at]
    created_at: Mapped[created_at]
    safety_reserve: Mapped[int | None]
    comment: Mapped[str]


class Shop(Base):
    short_name: Mapped[str]
    full_name: Mapped[str | None]
    ip_address: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")
