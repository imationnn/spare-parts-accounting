from sqlalchemy.orm import Mapped

from .base import Base


class Statuses:  # TODO добавить статусы
    pass


class PaymentMethods:
    cash = 1
    card = 2
    cashless = 3


class Status(Base):
    __tablename__ = "statuses"

    eng_name: Mapped[str]
    rus_name: Mapped[str]


class PaymentMethod(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
