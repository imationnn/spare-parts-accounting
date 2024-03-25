from sqlalchemy import ForeignKey
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base, created_at, int_def0, def_false
from .payment_method import PaymentMethods


class StatusOrders:
    new = {"rus_name": "Новый", "id": 1}
    awaitable = {"rus_name": "В ожидании", "id": 2}
    in_stock = {"rus_name": "На складе", "id": 3}
    completed = {"rus_name": "Выполнен", "id": 4}
    failure = {"rus_name": "Отказ", "id": 5}
    added = {"rus_name": "Добавлено", "id": 6}
    ordered = {"rus_name": "Заказано", "id": 7}
    in_receipt = {"rus_name": "В чеке", "id": 8}


class PhysicalOrder(Base):
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.new['id'],
                                           server_default=f"{StatusOrders.new['id']}")
    client_id: Mapped[int] = mapped_column(ForeignKey("physical_clients.id"))
    created_at: Mapped[created_at]
    prepayment: Mapped[Decimal] = mapped_column(default=0, server_default="0")
    total_price: Mapped[Decimal]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    is_print: Mapped[def_false]
    is_notify: Mapped[def_false]
    client_car_id: Mapped[int | None] = mapped_column(ForeignKey("client_cars.id"))
    comment: Mapped[str | None]


class JuridicalOrder(Base):
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.new['id'],
                                           server_default=f"{StatusOrders.new['id']}")
    client_id: Mapped[int] = mapped_column(ForeignKey("juridical_clients.id"))
    created_at: Mapped[created_at]
    prepayment: Mapped[Decimal] = mapped_column(default=0, server_default="0")
    total_price: Mapped[Decimal]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    is_print: Mapped[def_false]
    is_notify: Mapped[def_false]
    client_car_id: Mapped[int | None] = mapped_column(ForeignKey("client_cars.id"))
    comment: Mapped[str | None]


class PhysicalOrderDetail(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("catalog_parts.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.added['id'],
                                           server_default=f"{StatusOrders.added['id']}")
    qty_available: Mapped[int_def0]
    qty_needed: Mapped[int]
    order_id: Mapped[int] = mapped_column(ForeignKey("physical_orders.id"))
    employee_id: Mapped[int]
    price: Mapped[Decimal]
    supplier_id: Mapped[int | None]
    amount: Mapped[Decimal]
    sale: Mapped[int_def0]
    prepayment_part: Mapped[Decimal] = mapped_column(default=0, server_default="0")
    created_at: Mapped[created_at]
    change_time: Mapped[datetime | None]
    change_employee_id: Mapped[int | None]
    sales_receipt_id: Mapped[int | None]
    sale_id: Mapped[int | None]
    is_deleted: Mapped[def_false]
    comment: Mapped[str | None]


class JuridicalOrderDetail(Base):
    part_id: Mapped[int] = mapped_column(ForeignKey("catalog_parts.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status_orders.id"),
                                           default=StatusOrders.added['id'],
                                           server_default=f"{StatusOrders.added['id']}")
    qty_available: Mapped[int_def0]
    qty_needed: Mapped[int]
    order_id: Mapped[int] = mapped_column(ForeignKey("juridical_orders.id"))
    employee_id: Mapped[int]
    price: Mapped[Decimal]
    supplier_id: Mapped[int | None]
    amount: Mapped[Decimal]
    sale: Mapped[int_def0]
    prepayment_part: Mapped[Decimal] = mapped_column(default=0, server_default="0")
    created_at: Mapped[created_at]
    change_time: Mapped[datetime | None]
    change_employee_id: Mapped[int | None]
    sales_receipt_id: Mapped[int | None]
    sale_id: Mapped[int | None]
    is_deleted: Mapped[def_false]
    comment: Mapped[str | None]


class StatusOrder(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
