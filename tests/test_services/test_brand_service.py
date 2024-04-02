import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BrandNotFound, BrandAlreadyExist
from app.schemas import BrandId, BrandName, BrandNewIn, BrandNewOut, BrandUpdIn, BrandUpdOut
from app.services import BrandService


async def test_brand_by_name(session: AsyncSession):
    with pytest.raises(BrandNotFound):
        assert await BrandService(session).get_brand_by_name("")
    result = await BrandService(session).get_brand_by_name("Mazda")
    assert result == BrandId(id=4)


async def test_brand_by_id(session: AsyncSession):
    with pytest.raises(BrandNotFound):
        assert await BrandService(session).get_brand_by_id(100)
    result = await BrandService(session).get_brand_by_id(4)
    assert result == BrandName(brand_name="Mazda")


async def test_add_brand(session: AsyncSession):
    brand = BrandNewIn(brand_name="Mobil")
    with pytest.raises(BrandAlreadyExist):
        assert await BrandService(session).add_brand(brand)
    brand.brand_name = "Esso"
    result = await BrandService(session).add_brand(brand)
    assert result == BrandNewOut(brand_name="Esso", id=6)


async def test_edit_brand(session: AsyncSession):
    brand = BrandUpdIn(id=3, brand_name="Toyo")
    result = await BrandService(session).edit_brand(brand)
    assert result == BrandUpdOut(id=3, brand_name="Toyo")
    brand.brand_name = "Toyota"
    result = await BrandService(session).edit_brand(brand)
    assert result == BrandUpdOut(id=3, brand_name="Toyota")
    brand.brand_name = "Toyota"
    brand.id = 4
    with pytest.raises(BrandAlreadyExist):
        assert await BrandService(session).edit_brand(brand)
    brand.id = 40
    with pytest.raises(BrandNotFound):
        assert await BrandService(session).edit_brand(brand)

