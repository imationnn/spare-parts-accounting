from sqlalchemy import ForeignKey
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, int_def0, def_false
from .payment_method import PaymentMethods


class StatusOrders:  # TODO добавить статусы
    new = {"rus_name": "Новый", "id": 1}


class PhysicalOrder(Base):
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.new['id'],
                                           server_default=f"{StatusOrders.new['id']}")
    client_id: Mapped[int] = mapped_column(ForeignKey("physical_clients.id"))
    created_at: Mapped[created_at]
    prepayment: Mapped[int]
    total_price: Mapped[int_def0]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    is_print: Mapped[def_false]
    is_notify: Mapped[def_false]
    client_car_id: Mapped[int | None] = mapped_column(ForeignKey("client_cars.id"))


class JuridicalOrder(Base):
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.new['id'],
                                           server_default=f"{StatusOrders.new['id']}")
    client_id: Mapped[int] = mapped_column(ForeignKey("juridical_clients.id"))
    created_at: Mapped[created_at]
    prepayment: Mapped[int]
    total_price: Mapped[int_def0]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    is_print: Mapped[def_false]
    is_notify: Mapped[def_false]
    client_car_id: Mapped[int | None] = mapped_column(ForeignKey("client_cars.id"))


class StatusOrder(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
