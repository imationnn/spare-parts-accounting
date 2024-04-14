import os
import asyncio
import logging
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import db_connector, settings
from app.services import AuthHelper
from app.models import (StatusMovements,
                        StatusMovement,
                        MarginCategories,
                        MarginCategory,
                        Role,
                        Roles,
                        StatusOrders,
                        StatusOrder,
                        PaymentMethods,
                        PaymentMethod,
                        StatusReceipt,
                        StatusReceipts,
                        Employee)
from tests.create_data_for_tests import insert_test_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 30
WAIT_SECONDS = 1.5

TABLES = {
    StatusMovements: StatusMovement,
    Roles: Role,
    StatusOrders: StatusOrder,
    PaymentMethods: PaymentMethod,
    StatusReceipts: StatusReceipt
}


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
)
async def init_db(session: AsyncSession):
    try:
        await session.execute(select(1))
    except Exception as err:
        logger.error(err)
        raise err


async def add_static_data(session: AsyncSession):
    for source, model in TABLES.items():
        values = [model(eng_name=eng_name,
                        rus_name=value["rus_name"])
                  for eng_name, value in source.__dict__.items()
                  if not eng_name.startswith('__')]
        session.add_all(values)
        await session.commit()

    values = [MarginCategory(margin_value=value["value"])
              for eng_name, value in MarginCategories.__dict__.items()
              if not eng_name.startswith('__')]
    session.add_all(values)
    await session.commit()


async def create_first_user(session: AsyncSession):
    res = await session.execute(select(Employee))
    if res.first():
        return

    logger.info("Creating first employee")
    employee = Employee(login=settings.first_employee_login,
                        password=AuthHelper.get_hash_password(settings.first_employee_password),
                        full_name=settings.first_employee_fullname,
                        role_id=Roles.admin["id"])
    session.add(employee)
    await session.commit()


async def generate_all_values(session: AsyncSession):
    try:
        res = await session.execute(select(MarginCategory))
        if res.first():
            return
    except ProgrammingError:
        await session.rollback()
        logger.info("Creating tables")
        os.system("alembic upgrade head")

    logger.info("Generating needed data")
    await add_static_data(session)


async def generate_test_data(session: AsyncSession):
    res = await session.execute(select(Employee))
    if len(res.all()) > 1:
        return

    logger.info("Generating test data")
    await insert_test_data(session)


async def main():
    async with db_connector.session_factory() as session:
        logger.info("Initializing database")
        await init_db(session)
        await generate_all_values(session)
        await create_first_user(session)
        if settings.add_test_data:
            await generate_test_data(session)


if __name__ == '__main__':
    asyncio.run(main())
