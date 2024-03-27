from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ClientCar(Base):
    car_id: Mapped[int] = mapped_column(ForeignKey("catalog_cars.id"))
    vin_code: Mapped[str | None]
    comment: Mapped[str | None]
    physical_client_id: Mapped[int | None]
    juridical_client_id: Mapped[int | None]


class CatalogCar(Base):  # TODO придумать иерархию!
    pass
