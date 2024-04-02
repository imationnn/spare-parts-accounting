from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base, created_at, int_def0, def_false, num_20_2
from .payment_method import PaymentMethods


class StatusReceipts:
    not_paid = {"rus_name": "Не оплачен", "id": 1}
    paid = {"rus_name": "Оплачен", "id": 2}
    failure = {"rus_name": "Отказ", "id": 3}
    completed = {"rus_name": "Выдано", "id": 4}


class PhysicalSaleReceipt(Base):
    client_id: Mapped[int | None] = mapped_column(ForeignKey("physical_clients.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status_receipts.id"),
                                           default=StatusReceipts.not_paid['id'],
                                           server_default=f"{StatusReceipts.not_paid['id']}")
    total_price: Mapped[num_20_2]
    created_at: Mapped[created_at]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    client_car_id: Mapped[int | None]
    order_id: Mapped[int | None]
    is_deleted: Mapped[def_false]


class JuridicalSaleReceipt(Base):
    client_id: Mapped[int | None] = mapped_column(ForeignKey("juridical_clients.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status_receipts.id"),
                                           default=StatusReceipts.not_paid['id'],
                                           server_default=f"{StatusReceipts.not_paid['id']}")
    total_price: Mapped[num_20_2]
    created_at: Mapped[created_at]
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"),
                                                   default=PaymentMethods.cash['id'],
                                                   server_default=f"{PaymentMethods.cash['id']}")
    employee_id: Mapped[int]
    shop_id: Mapped[int]
    client_car_id: Mapped[int | None]
    order_id: Mapped[int | None]
    is_deleted: Mapped[def_false]


class PhysicalSaleReceiptDetail(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("actual_products.id"))
    qty_available: Mapped[int]
    qty_needed: Mapped[int]
    status_id: Mapped[int] = mapped_column(ForeignKey("status_receipts.id"),
                                           default=StatusReceipts.completed['id'],
                                           server_default=f"{StatusReceipts.completed['id']}")
    price: Mapped[num_20_2]
    amount: Mapped[num_20_2]
    sale: Mapped[int_def0]
    prepayment_part: Mapped[num_20_2 | None]
    employee_id: Mapped[int]
    paid_time: Mapped[datetime | None]
    order_id: Mapped[int | None]
    sale_id: Mapped[int] = mapped_column(ForeignKey("physical_sale_receipts.id"))
    order_det_id: Mapped[int | None]
    is_deleted: Mapped[def_false]


class JuridicalSaleReceiptDetail(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("actual_products.id"))
    qty_available: Mapped[int]
    qty_needed: Mapped[int]
    status_id: Mapped[int] = mapped_column(ForeignKey("status_receipts.id"),
                                           default=StatusReceipts.completed['id'],
                                           server_default=f"{StatusReceipts.completed['id']}")
    price: Mapped[num_20_2]
    amount: Mapped[num_20_2]
    sale: Mapped[int_def0]
    prepayment_part: Mapped[num_20_2 | None]
    employee_id: Mapped[int]
    paid_time: Mapped[datetime | None]
    order_id: Mapped[int | None]
    sale_id: Mapped[int] = mapped_column(ForeignKey("juridical_sale_receipts.id"))
    order_det_id: Mapped[int | None]
    is_deleted: Mapped[def_false]


class StatusReceipt(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
