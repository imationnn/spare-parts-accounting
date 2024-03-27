from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from app.models import Base


class BaseRepository:
    model: Base
    session: AsyncSession

    async def get_one(self, **filter_by) -> Base | None:
        stmt = select(self.model).filter_by(**filter_by)
        return await self.session.scalar(stmt)

    async def add_one(self, **data) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def add_all(self):
        pass

    async def edit_one(self, _id: int, **data) -> int:
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def edit_all(self):
        pass

    async def delete_one(self):
        pass

    async def delete_all(self):
        pass
