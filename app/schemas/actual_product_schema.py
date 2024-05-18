from datetime import datetime

from pydantic import BaseModel, Field

from app.models import num_20_2
from app.schemas import CatalogOutByNumber


class Shop(BaseModel):
    id: int
    short_name: str


class ActualProductOutById(BaseModel):
    id: int
    part_id: int
    price: num_20_2
    movement_id: int | None
    arrive_id: int
    created_at: datetime
    arrived_at: datetime
    comment: str | None


class ActualProductOutByPartId(BaseModel):
    id: int
    arrived: int
    released: int
    rest: int
    price: num_20_2
    reserve: int
    arrived_at: datetime
    safety_reserve: int | None
    shop: Shop
    part: CatalogOutByNumber


class ActualProductUpdateIn(BaseModel):
    price: num_20_2 | None = Field(default=None, ge=0)
    safety_reserve: int | None = Field(default=None, ge=0)
    comment: str | None = Field(default=None, max_length=200)


class ActualProductUpdateOut(ActualProductOutById):
    pass
