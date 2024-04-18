from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at, int_def0, num_20_2


if TYPE_CHECKING:
    from .catalog import CatalogPart


class ActualProduct(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("catalog_parts.id"))
    arrived: Mapped[int]
    released: Mapped[int_def0]
    rest: Mapped[int]
    price: Mapped[num_20_2]
    movement_id: Mapped[int | None]
    reserve: Mapped[int_def0]
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    arrive_id: Mapped[int] = mapped_column(ForeignKey("new_arrivals.id"))
    arrived_at: Mapped[created_at]
    created_at: Mapped[created_at]
    safety_reserve: Mapped[int | None]
    comment: Mapped[str | None]

    part: Mapped["CatalogPart"] = relationship(lazy='joined')


class Shop(Base):
    short_name: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str | None]
    ip_address: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")
