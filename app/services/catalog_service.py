import re

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, StatementError

from app.config import db_connector
from app.repositories import CatalogRepository
from app.schemas import CatalogOutById, CatalogOutByNumber, CatalogUpdIn, CatalogUpdOut, CatalogIn, CatalogInOut


class CatalogService(CatalogRepository):

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    @staticmethod
    def check_values(part: BaseModel) -> dict:
        values = part.model_dump(exclude_none=True)
        if not values:
            raise HTTPException(400)
        return values

    @staticmethod
    def normalize_number(number: str) -> str | None:
        result = re.sub('[^A-Za-z0-9]', '', number)
        if not result:
            return
        return result

    async def get_one_part_by_id(self, part_id: int) -> CatalogOutById:
        result = await self.get_one_part(part_id)
        if not result:
            raise HTTPException(404, detail="Нет такой детали")
        return CatalogOutById.model_validate(result, from_attributes=True)

    async def get_parts_by_number(self, number: str) -> list[CatalogOutByNumber]:
        number = self.normalize_number(number)
        result = await self.get_multi(limit=50, search_id=number)
        return [CatalogOutByNumber.model_validate(item, from_attributes=True) for item in result]

    async def update_part(self, part_id: int, part: CatalogUpdIn) -> CatalogUpdOut:
        values = self.check_values(part)

        if number := values.get("number"):
            values["search_id"] = self.normalize_number(number)

        try:
            result = await self.edit_one(part_id, **values)
            await self.session.commit()
        except (StatementError, NoResultFound):
            raise HTTPException(400)
        return CatalogUpdOut.model_validate(result, from_attributes=True)

    async def add_part(self, part: CatalogIn) -> CatalogInOut:
        values = self.check_values(part)
        values["search_id"] = self.normalize_number(values["number"])
        try:
            result = await self.add_one(**values)
            await self.session.commit()
        except (StatementError, NoResultFound):
            raise HTTPException(400)
        return CatalogInOut.model_validate(result, from_attributes=True)
