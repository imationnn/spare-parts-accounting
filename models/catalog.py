from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from .base import Base


class MarginCategories:
    category_1 = 1.4
    category_2 = 1.5
    category_3 = 1.6
    category_4 = 1.7
    category_5 = 1.8


class CatalogPart(Base):
    number: Mapped[str]
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    desc_eng: Mapped[str | None]
    desc_rus: Mapped[str]
    margin_id: Mapped[int] = mapped_column(ForeignKey("margin_categories.id"), default=1, server_default="1")
    search_id: Mapped[str]
    comment: Mapped[str | None]


class Brand(Base):
    brand_name: Mapped[str]


class MarginCategory(Base):
    __tablename__ = "margin_categories"

    margin_value: Mapped[Decimal]
