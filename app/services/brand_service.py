from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector
from app.exceptions import BrandNotFound, BrandAlreadyExist
from app.repositories import BrandRepository
from app.schemas import BrandUpdIn, BrandNewIn, BrandName, BrandId, BrandNewOut, BrandUpdOut


class BrandService(BrandRepository):

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def get_brand_by_name(self, brand_name: str) -> BrandId:
        result = await self.get_one(brand_name=brand_name)
        if not result:
            raise BrandNotFound
        return BrandId.model_validate(result, from_attributes=True)

    async def get_brand_by_id(self, brand_id: int) -> BrandName:
        result = await self.get_one(id=brand_id)
        if not result:
            raise BrandNotFound
        return BrandName.model_validate(result, from_attributes=True)

    async def add_brand(self, brand_new: BrandNewIn) -> BrandNewOut:
        if await self.get_one(brand_name=brand_new.brand_name):
            raise BrandAlreadyExist
        result = await self.add_one(brand_name=brand_new.brand_name)
        await self.session.commit()
        return BrandNewOut.model_validate(result, from_attributes=True)

    async def edit_brand(self, brand: BrandUpdIn) -> BrandUpdOut:
        await self.get_brand_by_id(brand.id)
        if await self.get_one(brand_name=brand.brand_name):
            raise BrandAlreadyExist
        result = await self.edit_one(brand.id, brand_name=brand.brand_name)
        await self.session.commit()
        return BrandUpdOut.model_validate(result, from_attributes=True)
