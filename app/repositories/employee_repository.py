from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Employee
from app.repositories import BaseRepository


class EmployeeRepository(BaseRepository):
    model = Employee

    async def get_employee(self, **filter_by) -> model | None:
        stmt = select(self.model).options(joinedload(self.model.role)).filter_by(**filter_by)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def get_all_users(self) -> Sequence[model]:
        stmt = select(self.model).options(joinedload(self.model.role))
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_employee(self, employee_id: int, **update):
        return await self.edit_one(employee_id, **update)
