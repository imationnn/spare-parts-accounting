from fastapi import APIRouter, Depends

from app.services import EmployeeService, CheckRole
from app.schemas import NewEmployee, EmployeeOut, EmployeeUpdIn, EmployeeUpdOut, NewEmployeeOut
from app.models import Roles

employee_router = APIRouter(
    prefix='/employee',
    tags=['Сотрудники'],
    dependencies=[Depends(CheckRole([
        Roles.admin["id"],
        Roles.director["id"]
    ]))])


@employee_router.get("/by-login",
                     summary='Получить информацию о сотруднике по логину')
async def get_employee_by_login(
        employee_login: str,
        employee_service: EmployeeService = Depends(EmployeeService)
) -> EmployeeOut:
    return await employee_service.get_employee_by_login(employee_login)


@employee_router.get("/by-id",
                     summary='Получить информацию о сотруднике по id')
async def get_employee_by_id(
        employee_id: int,
        employee_service: EmployeeService = Depends(EmployeeService)
) -> EmployeeOut:
    return await employee_service.get_employee_by_id(employee_id)


@employee_router.get("/all",
                     summary='Получить всех сотрудников')
async def get_all_employee(
        employee_service: EmployeeService = Depends(EmployeeService)
) -> list[EmployeeOut]:
    return await employee_service.get_all_employees()


@employee_router.post("/new",
                      summary='Добавить нового сотрудника')
async def add_new_employee(
        employee: NewEmployee,
        employee_service: EmployeeService = Depends(EmployeeService)
) -> NewEmployeeOut:
    return await employee_service.add_new_employee(employee)


@employee_router.put("/{employee_id}/edit",
                     summary='Изменить информацию о сотруднике')
async def edit_employee(
        employee_id: int,
        employee: EmployeeUpdIn,
        employee_service: EmployeeService = Depends(EmployeeService)
) -> EmployeeUpdOut:
    return await employee_service.edit_employee(employee_id, employee)
