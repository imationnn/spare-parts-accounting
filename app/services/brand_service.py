from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector
from app.exceptions import BrandNotFound, BrandAlreadyExist
from app.repositories import BrandRepository
from app.schemas import BrandInUpd


class BrandService(BrandRepository):

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def get_brand_by_name(self, brand_name: str):
        result = await self.get_one(brand_name=brand_name)
        if not result:
            raise BrandNotFound
        return result

    async def get_brand_by_id(self, brand_id: int):
        result = await self.get_one(id=brand_id)
        if not result:
            raise BrandNotFound
        return result

    async def add_brand(self, brand_name: str):
        if await self.get_one(brand_name=brand_name):
            raise BrandAlreadyExist
        return await self.add_one(brand_name=brand_name)

    async def edit_brand(self, brand: BrandInUpd):
        await self.get_brand_by_id(brand.id)
        return await self.edit_one(brand.id, brand_name=brand.brand_name)
