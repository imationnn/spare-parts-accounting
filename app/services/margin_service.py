from fastapi import Depends, HTTPException

from app.repositories import MarginRepository
from app.schemas import Margin


class MarginService:
    def __init__(self, repository: MarginRepository = Depends(MarginRepository)):
        self.repository = repository

    async def get_all_category(self) -> list[Margin]:
        result = await self.repository.get_multi()
        return [Margin.model_validate(item, from_attributes=True) for item in result]

    async def edit_margin_value(self, margin: Margin) -> Margin:
        if not await self.repository.get_one(id=margin.id):
            raise HTTPException(404, detail='Category not found')
        result = await self.repository.edit_one(margin.id, margin_value=margin.margin_value)
        await self.repository.session.commit()
        return Margin.model_validate(result, from_attributes=True)
