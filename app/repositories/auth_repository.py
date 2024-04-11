import dataclasses
import pickle

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Shop
from app.repositories import EmployeeRepository


@dataclasses.dataclass
class EmployeeCache:
    shop_id: int | None
    refresh_token: str


class AuthRepository(EmployeeRepository):
    redis: Redis

    async def get_user_by_login_for_auth(self, login: str, ip_address: str) -> list | None:
        stmt = (select(self.model, Shop)
                .options(joinedload(self.model.role))
                .outerjoin(Shop, Shop.ip_address == ip_address)
                .where(self.model.login == login))
        result = await self.session.execute(stmt)
        return result.one_or_none()

    async def create_employee_cache(self, employee_id: str | int, shop: Shop | None, refresh_token: str):
        if shop:
            shop = shop.id
        else:
            employee = await self.get_employee_cache(employee_id)
            if employee:
                shop = employee.shop_id
        emp_cache = EmployeeCache(shop_id=shop, refresh_token=refresh_token)
        await self.redis.set(str(employee_id), pickle.dumps(emp_cache))

    async def get_employee_cache(self, employee_id: str | int) -> EmployeeCache | None:
        emp_cache = await self.redis.get(str(employee_id))
        if emp_cache:
            return pickle.loads(emp_cache)

    async def update_employee_cache(self, employee_id: str | int, shop_id: int) -> EmployeeCache | None:
        emp_cache: EmployeeCache = await self.get_employee_cache(employee_id)
        if emp_cache:
            emp_cache.shop_id = shop_id
            await self.redis.set(str(employee_id), pickle.dumps(emp_cache))
        return emp_cache
