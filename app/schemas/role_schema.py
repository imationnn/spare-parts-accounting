from app.schemas.base_schema import BaseSchema


class RoleOut(BaseSchema):
    id: int
    rus_name: str
