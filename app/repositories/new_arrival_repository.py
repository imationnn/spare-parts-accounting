from datetime import datetime
from decimal import Decimal
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

    async def create_new_arrival(self, shop_id: int, employee_id: int, values: dict) -> model:
        return await self.add_one(shop_id=shop_id, employee_id=employee_id, **values)


class NewArrivalDetailRepository(BaseRepository):
    model = NewArrivalDetail

    async def add_new_arrive_detail(
            self,
            part_id: int,
            qty: int,
            price_in: Decimal,
            price_out: Decimal,
            amount: Decimal,
            employee_id: int,
            ccd: str,
            arrive_id: int
    ) -> model:
        return await self.add_one(
            part_id=part_id,
            qty=qty,
            price_in=price_in,
            price_out=price_out,
            amount=amount,
            employee_id=employee_id,
            ccd=ccd,
            arrive_id=arrive_id
        )
