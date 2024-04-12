from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import CatalogPart
from app.repositories import BaseRepository


class CatalogRepository(BaseRepository):
    model = CatalogPart

    async def get_one_part(self, part_id: int) -> model:
        """
        Takes part id and returns model CatalogPart with brand and margins.
        :param part_id:
        :return:
        """
        stmt = select(self.model).options(joinedload(self.model.margin)).where(self.model.id == part_id)
        return await self.session.scalar(stmt)
