from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, int_def0, def_false


class Supplier(Base):
    org_name: Mapped[str]
    org_attr_id: Mapped[int | None] = mapped_column(ForeignKey("org_attrs.id"))


class PhysicalClient(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str | None]
    phone: Mapped[str | None]
    email: Mapped[str | None]
    sale: Mapped[int_def0]
    sale_card: Mapped[str | None] = mapped_column(unique=True)
    comment: Mapped[str | None]
    is_black_list: Mapped[def_false]


class JuridicalClient(Base):
    org_name: Mapped[str]
    sale: Mapped[int_def0]
    sale_card: Mapped[str | None] = mapped_column(unique=True)
    phone: Mapped[str | None]
    comment: Mapped[str | None]
    is_black_list: Mapped[def_false]
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
