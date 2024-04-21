from pydantic import BaseModel, Field


class BrandId(BaseModel):
    id: int = Field(ge=1)


class BrandNewIn(BaseModel):
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
