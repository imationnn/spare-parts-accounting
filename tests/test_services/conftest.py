import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import BrandService
from app.repositories import BrandRepository


@pytest.fixture(scope="module")
async def brand_service(session: AsyncSession):
    return BrandService(BrandRepository(session=session))
