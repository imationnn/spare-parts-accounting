from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

from app.config import db_connector
from app.models import Base


class BaseRepository:
    model: type[Base]

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def get_one(self, **filter_by) -> Base | None:
        stmt = select(self.model).filter_by(**filter_by)
        return await self.session.scalar(stmt)

    async def get_multi(self, order: str = "id", limit: int = 100, offset: int = 0, **filter_by) -> Sequence:
        stmt = select(self.model).filter_by(**filter_by).order_by(order).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def add_one(self, **data):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit_one(self, _id: int, **data):
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_one(self, _id: int):
        stmt = delete(self.model).where(self.model.id == _id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
