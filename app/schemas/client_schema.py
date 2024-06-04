from pydantic import BaseModel, Field


class PhysicalClientIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    patronymic: str | None = Field(default=None, min_length=2, max_length=30)
    phone: str | None = Field(default=None, examples=["+7-900-111-11-11"])
    email: str | None = Field(default=None)
    sale: int = Field(default=0, ge=0)
    sale_card: str | None = Field(default=None)
    comment: str | None = Field(default=None, max_length=300)
    is_black_list: bool = Field(default=False)


class PhysicalClientOut(PhysicalClientIn):
    id: int
