from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException


class PhysicalClientIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    patronymic: str | None = Field(default=None, min_length=1, max_length=30)
    phone: str | None = Field(default=None, examples=["+7-900-111-11-11"])
    email: str | None = Field(default=None)
    sale: int = Field(default=0, ge=0)
    sale_card: str | None = Field(default=None)
    comment: str | None = Field(default=None, max_length=300)
    is_black_list: bool = Field(default=False)

    @field_validator("first_name", "last_name", "patronymic", "phone", "email", "sale_card")
    def strip_whitespaces(cls, field: str) -> str:
        if field is not None:
            strip_field = field.strip()
            if strip_field:
                return strip_field
            raise HTTPException(422, detail="String should have at least 1 characters")


class PhysicalClientOut(PhysicalClientIn):
    id: int
