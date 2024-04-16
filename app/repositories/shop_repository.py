from typing import Sequence

from app.models import Shop, Base
from app.repositories import BaseRepository


class ShopRepository(BaseRepository):
    model = Shop

    async def get_shop(self, **filter_by) -> model | None:
        return await self.get_one(**filter_by)

    async def get_all_shops(self) -> Sequence[model | Base]:
        return await self.get_multi()

    async def add_shop(self, **data):
        return await self.add_one(**data)

    async def edit_shop(self, shop_id: int, **data):
        return await self.edit_one(shop_id, **data)
