from pydantic import BaseModel, Field


class OrgAttr(BaseModel):
    inn: str | None = None
    ogrn: str | None = None
    kpp: str | None = None
    okved: str | None = None
    address: str | None = None
    bank_name: str | None = None
    bik: str | None = None
    r_s: str | None = None


class SupplierIn(BaseModel):
    org_name: str = Field(min_length=2, max_length=50)
    org_attr: OrgAttr


class SupplierOut(SupplierIn):
    id: int
    org_attr_id: int | None
