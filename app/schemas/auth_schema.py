from app.schemas import BaseSchema


class Tokens(BaseSchema):
    access_token: str
    refresh_token: str | None = None
    type: str = "Bearer"


class GetMe(BaseSchema):
    employee_id: int
    shop_id: int | None
    role_id: int
