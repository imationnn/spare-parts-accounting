from decimal import Decimal

from pydantic import Field

from app.schemas import BaseSchema


class Margin(BaseSchema):
    id: int = Field(ge=1)
    margin_value: Decimal = Field(ge=1, decimal_places=2)
