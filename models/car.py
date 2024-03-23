from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ClientCar(Base):
    car_id: Mapped[int] = mapped_column(ForeignKey("catalog_cars.id"))
    vin_code: Mapped[str | None]
    comment: Mapped[str | None]
    client_id: Mapped[int]


class CatalogCar(Base):  # TODO придумать иерархию!
    pass
