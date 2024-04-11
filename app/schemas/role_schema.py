from pydantic import BaseModel


class RoleOut(BaseModel):
    id: int
    rus_name: str
