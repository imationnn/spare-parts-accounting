from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, num_20_2


class StatusMovements:
    created = {"rus_name": "Создано", "id": 1}
    sent = {"rus_name": "Отправлено", "id": 2}
    deleted = {"rus_name": "Удалено", "id": 3}
    accepted = {"rus_name": "Принято", "id": 4}
    on_transit = {"rus_name": "В пути", "id": 5}
    added = {"rus_name": "Добавлено", "id": 6}
    completed = {"rus_name": "Выдано", "id": 7}


class IncomingMovement(Base):
    from_shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    to_shop_id: Mapped[int]
    status: Mapped[int] = mapped_column(ForeignKey("status_movements.id"),
                                        default=StatusMovements.on_transit['id'],
                                        server_default=f"{StatusMovements.on_transit['id']}")
    created_at: Mapped[created_at]
    arrived_at: Mapped[datetime | None]
    created_employee_id: Mapped[int]
    accepted_employee_id: Mapped[int | None]
    total_price: Mapped[num_20_2]


class OutgoingMovement(Base):
    from_shop_id: Mapped[int]
    to_shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    status: Mapped[int] = mapped_column(ForeignKey("status_movements.id"),
                                        default=StatusMovements.created['id'],
                                        server_default=f"{StatusMovements.created['id']}")
    created_at: Mapped[created_at]
    sent_at: Mapped[datetime | None]
    created_employee_id: Mapped[int]
    total_price: Mapped[num_20_2]


class IncomingMovementDetail(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("actual_products.id"))
    status: Mapped[int] = mapped_column(ForeignKey("status_movements.id"),
                                        default=StatusMovements.on_transit['id'],
                                        server_default=f"{StatusMovements.on_transit['id']}")
    qty: Mapped[int]
    amount: Mapped[num_20_2]
    move_id: Mapped[int] = mapped_column(ForeignKey("incoming_movements.id"))
    employee_id: Mapped[int]


class OutgoingMovementDetail(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("actual_products.id"))
    status: Mapped[int] = mapped_column(ForeignKey("status_movements.id"),
                                        default=StatusMovements.added['id'],
                                        server_default=f"{StatusMovements.added['id']}")
    qty: Mapped[int]
    amount: Mapped[num_20_2]
    created_at: Mapped[created_at]
    move_id: Mapped[int] = mapped_column(ForeignKey("outgoing_movements.id", ondelete="CASCADE"))
    employee_id: Mapped[int]


class StatusMovement(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
