from app.models import ActualProduct
from app.repositories import BaseRepository


class ActualProductRepository(BaseRepository):
    model = ActualProduct

    async def add_new_products(self, list_models: list[model]):
        self.session.add_all(list_models)

    async def get_actual_product(self, product_id: int) -> model | None:
        return await self.get_one(id=product_id)
