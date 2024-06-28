from app.schemas import BaseSchema


class ShopIn(BaseSchema):
    short_name: str
    full_name: str | None = None
    ip_address: str
    is_active: bool


class ShopUpd(BaseSchema):
    short_name: str | None = None
    full_name: str | None = None
    ip_address: str | None = None
    is_active: bool | None = None


class ShopOut(ShopIn):
    id: int


class ShopDelete(ShopUpd):
    id: int
