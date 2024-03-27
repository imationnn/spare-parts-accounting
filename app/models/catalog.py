from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from .base import Base


class MarginCategories:
    category_1 = {"value": 1.4, "id": 1}
    category_2 = {"value": 1.5, "id": 2}
    category_3 = {"value": 1.6, "id": 3}
    category_4 = {"value": 1.7, "id": 4}
    category_5 = {"value": 1.8, "id": 5}


class CatalogPart(Base):
    number: Mapped[str]
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    desc_eng: Mapped[str | None]
    desc_rus: Mapped[str]
    margin_id: Mapped[int] = mapped_column(ForeignKey("margin_categories.id"),
                                           default=MarginCategories.category_1['id'],
                                           server_default=f"{MarginCategories.category_1['id']}")
    search_id: Mapped[str]
    comment: Mapped[str | None]


class Brand(Base):
    brand_name: Mapped[str]


class MarginCategory(Base):
    __tablename__ = "margin_categories"

    margin_value: Mapped[Decimal]
