import re

from fastapi import Depends
from sqlalchemy.exc import NoResultFound, StatementError

from app.repositories import CatalogRepository
from app.schemas import (CatalogOutById,
                         CatalogOutByNumber,
                         CatalogUpdIn,
                         CatalogUpdOut,
                         CatalogIn,
                         CatalogInOut,
                         CatalogDelete)
from app.exceptions import PartNotFound, PartBadParameters, PartCannotBeDeleted


class CatalogService:

    def __init__(self, repository: CatalogRepository = Depends()):
        self.repository = repository

    @staticmethod
    def normalize_number(number: str) -> str | None:
        result = re.sub('[^A-Za-z0-9]', '', number)
        if result:
            return result

    async def get_one_part_by_id(self, part_id: int) -> CatalogOutById:
        result = await self.repository.get_one_part(part_id)
        if not result:
            raise PartNotFound
        return CatalogOutById.model_validate(result)

    async def get_parts_by_number(self, number: str) -> list[CatalogOutByNumber]:
        number = self.normalize_number(number)
        result = await self.repository.get_multi(limit=50, search_id=number)
        return [CatalogOutByNumber.model_validate(item) for item in result]

    async def update_part(self, part_id: int, part: CatalogUpdIn) -> CatalogUpdOut:
        values = part.model_dump(exclude_unset=True)
        if not values:
            raise PartBadParameters

        if part.number:
            values["search_id"] = self.normalize_number(part.number)

        try:
            result = await self.repository.edit_one(part_id, **values)
            await self.repository.session.commit()
        except StatementError:
            raise PartBadParameters
        except NoResultFound:
            raise PartNotFound
        return CatalogUpdOut.model_validate(result)

    async def add_part(self, part: CatalogIn) -> CatalogInOut:
        values = part.model_dump(exclude_none=True)
        values["search_id"] = self.normalize_number(part.number)
        try:
            result = await self.repository.add_one(**values)
            await self.repository.session.commit()
        except StatementError:
            raise PartBadParameters
        return CatalogInOut.model_validate(result)

    async def delete_part(self, part_id: int) -> CatalogDelete:
        try:
            result = await self.repository.delete_one(part_id)
            await self.repository.session.commit()
        except StatementError:
            raise PartCannotBeDeleted
        except NoResultFound:
            raise PartNotFound
        return CatalogDelete.model_validate(result)
