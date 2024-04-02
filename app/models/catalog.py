from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, num_20_2


class MarginCategories:
    category_1 = {"value": 1.4, "id": 1}
    category_2 = {"value": 1.5, "id": 2}
    category_3 = {"value": 1.6, "id": 3}
    category_4 = {"value": 1.7, "id": 4}
    category_5 = {"value": 1.8, "id": 5}


class CatalogPart(Base):
    __table_args__ = (
        UniqueConstraint(
            "number",
            "brand_id",
            name="catalog_parts_unique"),
    )
    number: Mapped[str]
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    desc_eng: Mapped[str | None]
    desc_rus: Mapped[str]
    margin_id: Mapped[int] = mapped_column(ForeignKey("margin_categories.id"),
                                           default=MarginCategories.category_1['id'],
                                           server_default=f"{MarginCategories.category_1['id']}")
    search_id: Mapped[str]
    comment: Mapped[str | None]

    brand: Mapped["Brand"] = relationship(lazy='joined')
    margin: Mapped["MarginCategory"] = relationship()


class Brand(Base):
    brand_name: Mapped[str]


class MarginCategory(Base):
    __tablename__ = "margin_categories"

    margin_value: Mapped[num_20_2]
