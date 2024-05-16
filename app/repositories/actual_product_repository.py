from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import ActualProduct
from app.repositories import BaseRepository


class ActualProductRepository(BaseRepository):
    model = ActualProduct

    async def add_new_products(self, list_models: list[model]):
        self.session.add_all(list_models)

    async def get_actual_product(self, product_id: int) -> model | None:
        return await self.get_one(id=product_id)

    async def get_list_actual_products(self, parts_id: list) -> Sequence[model]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.part), joinedload(self.model.shop))
            .where(self.model.part_id.in_(parts_id))
            .where(self.model.released != self.model.arrived)
            .order_by(self.model.part_id, self.model.arrived_at)
        )
        result = await self.session.scalars(stmt)
        return result.all()
