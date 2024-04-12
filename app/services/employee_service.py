from fastapi import Depends
from sqlalchemy.exc import StatementError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector
from app.repositories import EmployeeRepository
from app.schemas import NewEmployee, EmployeeOut, EmployeeUpdIn, EmployeeUpdOut, NewEmployeeOut
from app.services import AuthHelper
from app.exceptions import EmployeeAlreadyExist, EmployeeBadParameters, EmployeeNotFound


class EmployeeService(EmployeeRepository):

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def get_employee_by_login(self, login: str) -> EmployeeOut:
        employee = await self.get_employee(login=login)
        if not employee:
            raise EmployeeNotFound
        return EmployeeOut.model_validate(employee, from_attributes=True)

    async def get_employee_by_id(self, employee_id: int) -> EmployeeOut:
        employee = await self.get_employee(id=employee_id)
        if not employee:
            raise EmployeeNotFound
        return EmployeeOut.model_validate(employee, from_attributes=True)

    async def get_all_employees(self) -> list[EmployeeOut]:
        employees = await self.get_all_users()
        return [EmployeeOut.model_validate(employee, from_attributes=True) for employee in employees]

    async def add_new_employee(self, employee: NewEmployee) -> NewEmployeeOut:
        if await self.get_employee(login=employee.login):
            raise EmployeeAlreadyExist
        values = employee.model_dump(exclude_none=True)
        values["password"] = AuthHelper.get_hash_password(values["password"])
        try:
            result = await self.add_one(**values)
            await self.session.commit()
        except (StatementError, NoResultFound):
            raise EmployeeBadParameters
        return NewEmployeeOut.model_validate(result, from_attributes=True)

    async def edit_employee(self, employee_id: int, employee: EmployeeUpdIn) -> EmployeeUpdOut:
        values = employee.model_dump(exclude_none=True)
        if not values:
            raise EmployeeBadParameters

        if password := values.get("password"):
            values["password"] = AuthHelper.get_hash_password(password)

        try:
            result = await self.update_employee(employee_id, **values)
            await self.session.commit()
        except (StatementError, NoResultFound):
            raise EmployeeBadParameters
        return EmployeeUpdOut.model_validate(result, from_attributes=True)
