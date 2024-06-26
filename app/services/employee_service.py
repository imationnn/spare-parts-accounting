from fastapi import Depends
from sqlalchemy.exc import StatementError, NoResultFound

from app.repositories import EmployeeRepository
from app.schemas import NewEmployee, EmployeeOut, EmployeeUpdIn, EmployeeUpdOut, NewEmployeeOut
from app.services import AuthHelper
from app.exceptions import EmployeeAlreadyExist, EmployeeBadParameters, EmployeeNotFound


class EmployeeService:

    def __init__(self, repository: EmployeeRepository = Depends()):
        self.repository = repository

    async def get_employee_by_login(self, login: str) -> EmployeeOut:
        employee = await self.repository.get_employee(login=login)
        if not employee:
            raise EmployeeNotFound
        return EmployeeOut.model_validate(employee)

    async def get_employee_by_id(self, employee_id: int) -> EmployeeOut:
        employee = await self.repository.get_employee(id=employee_id)
        if not employee:
            raise EmployeeNotFound
        return EmployeeOut.model_validate(employee)

    async def get_all_employees(self) -> list[EmployeeOut]:
        employees = await self.repository.get_all_users()
        return [EmployeeOut.model_validate(employee) for employee in employees]

    async def add_new_employee(self, employee: NewEmployee) -> NewEmployeeOut:
        if await self.repository.get_employee(login=employee.login):
            raise EmployeeAlreadyExist
        employee.password = AuthHelper.get_hash_password(employee.password)
        try:
            result = await self.repository.add_one(**employee.model_dump(exclude_none=True))
            await self.repository.session.commit()
        except StatementError:
            raise EmployeeBadParameters
        return NewEmployeeOut.model_validate(result)

    async def edit_employee(self, employee_id: int, employee: EmployeeUpdIn) -> EmployeeUpdOut:
        values = employee.model_dump(exclude_unset=True)
        if not values:
            raise EmployeeBadParameters

        if employee.password:
            values["password"] = AuthHelper.get_hash_password(employee.password)

        try:
            result = await self.repository.update_employee(employee_id, **values)
            await self.repository.session.commit()
        except StatementError:
            raise EmployeeBadParameters
        except NoResultFound:
            raise EmployeeNotFound
        return EmployeeUpdOut.model_validate(result)
