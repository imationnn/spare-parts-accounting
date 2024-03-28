from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector
from app.repositories import MarginRepository
from app.schemas import Margin


class MarginService(MarginRepository):
    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.session = session

    async def get_all_category(self) -> list[Margin]:
        result = await self.get_multi()
        return [Margin.model_validate(item, from_attributes=True) for item in result]

    async def edit_margin_value(self, margin: Margin) -> Margin:
        if not await self.get_one(id=margin.id):
            raise HTTPException(404, detail='Нет такой категории')
        from_base = await self.edit_one(margin.id, margin_value=margin.margin_value)
        result = Margin.model_validate(from_base, from_attributes=True)
        await self.session.commit()
        return result
