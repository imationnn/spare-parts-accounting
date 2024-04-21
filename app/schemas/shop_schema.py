from pydantic import BaseModel


class ShopIn(BaseModel):
    short_name: str
    full_name: str | None = None
    ip_address: str
    is_active: bool


class ShopUpd(BaseModel):
    short_name: str | None = None
    full_name: str | None = None
    ip_address: str | None = None
    is_active: bool | None = None


class ShopOut(ShopIn):
    id: int


class ShopDelete(ShopUpd):
    id: int
