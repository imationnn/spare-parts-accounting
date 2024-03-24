from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Roles:
    admin = 1
    director = 2
    manager = 3


class Role(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str | None]


class Employee(Base):
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name: Mapped[str]
    phone: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=Roles.manager, server_default=f"{Roles.manager}")
    refresh_token: Mapped[str | None]
