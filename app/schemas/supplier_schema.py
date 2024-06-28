from pydantic import Field

from app.schemas import BaseSchema


class OrgAttr(BaseSchema):
    inn: str | None = None
    ogrn: str | None = None
    kpp: str | None = None
    okved: str | None = None
    address: str | None = None
    bank_name: str | None = None
    bik: str | None = None
    r_s: str | None = None


class SupplierIn(BaseSchema):
    org_name: str = Field(min_length=2, max_length=50)
    org_attr: OrgAttr


class SupplierOut(SupplierIn):
    id: int
    org_attr_id: int


class SupplierListOut(BaseSchema):
    id: int
    org_name: str
    org_attr_id: int


class SupplierUpdate(SupplierIn):
    org_name: str | None = None
