from pydantic import Field

from app.schemas import BaseSchema


class BrandId(BaseSchema):
    id: int = Field(ge=1)


class BrandNewIn(BaseSchema):
    brand_name: str = Field(min_length=2, max_length=15)


class BrandNewOut(BrandNewIn, BrandId):
    pass


class BrandName(BrandNewIn):
    pass


class BrandUpdIn(BrandNewIn, BrandId):
    pass


class BrandUpdOut(BrandNewIn, BrandId):
    pass


class BrandDelete(BrandNewOut):
    pass
