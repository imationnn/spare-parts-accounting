from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: str
    refresh_token: str | None = None
    type: str = "Bearer"


class GetMe(BaseModel):
    employee_id: int
    shop_id: int | None
    role_id: int
