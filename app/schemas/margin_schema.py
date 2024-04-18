from decimal import Decimal

from pydantic import BaseModel, Field


class Margin(BaseModel):
    id: int = Field(ge=1)
    margin_value: Decimal = Field(ge=1, decimal_places=2)
