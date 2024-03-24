from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Supplier(Base):
    org_name: Mapped[str]
    org_attr_id: Mapped[int | None] = mapped_column(ForeignKey("org_attrs.id"))


class Client(Base):
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    patronymic: Mapped[str | None]
    phone: Mapped[str | None]
    email: Mapped[str | None]
    sale: Mapped[int | None] = mapped_column(default=0, server_default="0")
    sale_card: Mapped[str | None] = mapped_column(unique=True)
    comment: Mapped[str | None]
    is_black_list: Mapped[bool] = mapped_column(default=False, server_default="False")
    org_name: Mapped[str | None]
    org_attr_id: Mapped[int | None] = mapped_column(ForeignKey("org_attrs.id"))


class OrgAttr(Base):
    inn: Mapped[str | None]
    ogrn: Mapped[str | None]
    kpp: Mapped[str | None]
    okved: Mapped[str | None]
    address: Mapped[str | None]
    bank_name: Mapped[str | None]
    bik: Mapped[str | None]
    r_s: Mapped[str | None]
