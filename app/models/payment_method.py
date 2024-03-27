from sqlalchemy.orm import Mapped

from .base import Base


class PaymentMethods:
    cash = {"rus_name": "Наличный расчет", "id": 1}
    card = {"rus_name": "Платежная карта", "id": 2}
    cashless = {"rus_name": "Безналичный расчет", "id": 3}


class PaymentMethod(Base):
    eng_name: Mapped[str]
    rus_name: Mapped[str]
