from pydantic import BaseModel


class BrandInUpd(BaseModel):
    id: int
    brand_name: str
