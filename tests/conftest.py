import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import PGConfig, db_connector
from app.config.database import PGDatabase
from main import app
from app.models import Base


pg_config = PGConfig()
pg_config.pg_db_name = os.getenv('PG_TEST_DB_NAME')
test_db_connector = PGDatabase(pg_config)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_db_connector.session_factory() as session:
        yield session


app.dependency_overrides[db_connector.get_session] = override_get_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database_value():
    from .create_data_for_tests import insert_test_data
    from pre_start import add_static_data
    async with test_db_connector.session_factory() as async_session:
        await add_static_data(async_session)
        await insert_test_data(async_session)


@pytest.fixture(scope='module')
async def session() -> AsyncSession:
    async with test_db_connector.session_factory() as session:
        yield session


@pytest.fixture(scope="session")
async def authclient() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as client:
        yield client


@pytest.fixture(scope="session")
async def header(authclient: AsyncClient):
    from tests.data_for_test import employees
    data = {'username': employees[0]["login"], 'password': employees[0]["password"]}
    resp = await authclient.post("/auth/login", data=data)
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
