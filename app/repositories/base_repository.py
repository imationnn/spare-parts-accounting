from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from app.models import Base


class BaseRepository:
    model: type[Base]
    session: AsyncSession

    async def get_one(self, **filter_by) -> Base | None:
        stmt = select(self.model).filter_by(**filter_by)
        return await self.session.scalar(stmt)

    async def get_multi(self, order: str = "id", limit: int = 100, offset: int = 0, **filter_by) -> Sequence[Base]:
        stmt = select(self.model).filter_by(**filter_by).order_by(order).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def add_one(self, **data) -> Base:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit_one(self, _id: int, **data) -> Base:
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
