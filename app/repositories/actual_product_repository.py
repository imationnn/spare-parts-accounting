from app.models import ActualProduct
from app.repositories import BaseRepository


class ActualProductRepository(BaseRepository):
    model = ActualProduct

    async def add_new_products(self, list_models: list[model]):
        self.session.add_all(list_models)
