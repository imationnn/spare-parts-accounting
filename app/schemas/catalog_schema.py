from pydantic import BaseModel, Field

from .brand_schema import BrandNewOut
from .margin_schema import Margin


class Catalog(BaseModel):
    number: str
    desc_eng: str | None
    desc_rus: str


class CatalogIn(BaseModel):
    number: str = Field(min_length=2, max_length=30)
    brand_id: int
    desc_eng: str | None = Field(default=None, max_length=100)
    desc_rus: str = Field(max_length=100)
    margin_id: int | None = None
    comment: str | None = Field(default=None, max_length=200)


class CatalogOutById(Catalog):
    id: int
    brand: BrandNewOut
    margin: Margin
    comment: str | None


class CatalogOutByNumber(Catalog):
    id: int
    brand: BrandNewOut


class CatalogUpdIn(BaseModel):
    number: str | None = Field(default=None, min_length=2, max_length=30)
    brand_id: int | None = None
    desc_eng: str | None = Field(default=None, max_length=100)
    desc_rus: str | None = Field(default=None, max_length=100)
    margin_id: int | None = None
    comment: str | None = Field(default=None, max_length=200)


class CatalogUpdOut(Catalog):
    id: int
    brand_id: int
    margin_id: int | None
    comment: str | None


class CatalogInOut(CatalogUpdOut):
    pass


class CatalogDelete(CatalogUpdIn):
    pass
