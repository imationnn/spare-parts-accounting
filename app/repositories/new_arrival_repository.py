import datetime
from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from app.repositories import BaseRepository
from app.models import NewArrival, NewArrivalDetail


class NewArrivalRepository(BaseRepository):
    model = NewArrival

    async def get_arrivals(
            self,
            start_from_date: datetime.datetime,
            shop_id: int,
            is_transferred: bool | None,
            order: str,
            limit: int,
            offset: int
    ) -> Sequence[model | None]:
        stmt = (select(self.model)
                .options(joinedload(self.model.employee), joinedload(self.model.supplier))
                .filter(and_(self.model.created_at > start_from_date, self.model.shop_id == shop_id))
                .order_by(order)
                .limit(limit)
                .offset(offset))
        if is_transferred is not None:
            stmt = stmt.filter(self.model.is_transferred == is_transferred)
        result = await self.session.scalars(stmt)
        return result.all()


class NewArrivalDetailRepository(BaseRepository):
    model = NewArrivalDetail
