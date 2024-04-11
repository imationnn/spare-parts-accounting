from pydantic import BaseModel

from .role_schema import RoleOut


class EmployeeOut(BaseModel):
    id: int
    login: str
    full_name: str
    phone: str | None
    is_active: bool
    role: RoleOut


class NewEmployee(BaseModel):
    login: str
    password: str
    full_name: str
    phone: str | None = None
    role_id: int | None = None


class EmployeeUpdOut(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    is_active: bool | None = None
    role_id: int | None = None


class EmployeeUpdIn(EmployeeUpdOut):
    password: str | None = None


class NewEmployeeOut(EmployeeUpdOut):
    id: int
    login: str
