from datetime import datetime
from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from app.repositories import BaseRepository
from app.models import NewArrival, NewArrivalDetail


class NewArrivalRepository(BaseRepository):
    model = NewArrival

    async def get_arrivals(
            self,
            from_date: datetime,
            to_date: datetime,
            shop_id: int,
            is_transferred: bool | None,
            sort_by: str,
            limit: int,
            offset: int
    ) -> Sequence[model | None]:
        stmt = (select(self.model)
                .options(joinedload(self.model.employee), joinedload(self.model.supplier))
                .filter(and_(self.model.created_at.between(from_date, to_date), self.model.shop_id == shop_id))
                .order_by(sort_by)
                .limit(limit)
                .offset(offset))
        if is_transferred is not None:
            stmt = stmt.filter(self.model.is_transferred == is_transferred)
        result = await self.session.scalars(stmt)
        return result.all()


class NewArrivalDetailRepository(BaseRepository):
    model = NewArrivalDetail
