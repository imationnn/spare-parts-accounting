from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Roles:
    admin = {"rus_name": "Администратор", "id": 1}
    director = {"rus_name": "Директор", "id": 2}
    manager = {"rus_name": "Менеджер", "id": 3}


class Role(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]


class Employee(Base):
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    full_name: Mapped[str]
    phone: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'),
                                         default=Roles.manager['id'],
                                         server_default=f"{Roles.manager['id']}")

    role: Mapped["Role"] = relationship()
