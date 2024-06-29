from fastapi import Depends
from sqlalchemy.exc import NoResultFound, StatementError

from app.exceptions import BrandNotFound, BrandAlreadyExist, BrandCannotBeDeleted
from app.repositories import BrandRepository
from app.schemas import BrandUpdIn, BrandNewIn, BrandName, BrandId, BrandNewOut, BrandUpdOut, BrandDelete


class BrandService:

    def __init__(self, repository: BrandRepository = Depends()):
        self.repository = repository

    async def get_brand_by_name(self, brand_name: str) -> BrandId:
        result = await self.repository.get_one(brand_name=brand_name)
        if not result:
            raise BrandNotFound
        return BrandId.model_validate(result)

    async def get_brand_by_id(self, brand_id: int) -> BrandName:
        result = await self.repository.get_one(id=brand_id)
        if not result:
            raise BrandNotFound
        return BrandName.model_validate(result)

    async def add_brand(self, brand_new: BrandNewIn) -> BrandNewOut:
        if await self.repository.get_one(brand_name=brand_new.brand_name):
            raise BrandAlreadyExist
        result = await self.repository.add_one(brand_name=brand_new.brand_name)
        await self.repository.session.commit()
        return BrandNewOut.model_validate(result)

    async def edit_brand(self, brand: BrandUpdIn) -> BrandUpdOut:
        await self.get_brand_by_id(brand.id)
        if await self.repository.get_one(brand_name=brand.brand_name):
            raise BrandAlreadyExist
        result = await self.repository.edit_one(brand.id, brand_name=brand.brand_name)
        await self.repository.session.commit()
        return BrandUpdOut.model_validate(result)

    async def delete_brand(self, brand_id: int) -> BrandDelete:
        try:
            result = await self.repository.delete_one(brand_id)
            await self.repository.session.commit()
        except NoResultFound:
            raise BrandNotFound
        except StatementError:
            raise BrandCannotBeDeleted
        return BrandDelete.model_validate(result)
