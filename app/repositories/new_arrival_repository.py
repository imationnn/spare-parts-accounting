from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload

from app.repositories import BaseRepository
from app.models import NewArrival, NewArrivalDetail, CatalogPart


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

    async def get_arrival_by_id(self, arrive_id: int) -> model:
        return await self.session.scalar(select(self.model).where(self.model.id == arrive_id))

    async def update_arrival(self, arrive_id: int, **values) -> model:
        return await self.edit_one(arrive_id, **values)

    async def delete_arrival(self, arrive_model: model):
        await self.session.delete(arrive_model)
        await self.session.commit()


class NewArrivalDetailRepository(BaseRepository):
    model = NewArrivalDetail

    async def add_new_arrive_detail(
            self,
            part_id: int,
            qty: int,
            price_in: Decimal,
            amount: Decimal,
            employee_id: int,
            ccd: str,
            arrive_id: int
    ) -> model:
        return await self.add_one(
            part_id=part_id,
            qty=qty,
            price_in=price_in,
            amount=amount,
            employee_id=employee_id,
            ccd=ccd,
            arrive_id=arrive_id
        )

    async def get_list_arrival_details(self, arrival_id: int) -> Sequence[model]:
        stmt = (select(self.model)
                .options(joinedload(self.model.employee), joinedload(self.model.part))
                .where(self.model.arrive_id == arrival_id))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_total_amount_arrival_details(self, arrival_id: int) -> Decimal:
        stmt = select(func.sum(self.model.amount)).where(self.model.arrive_id == arrival_id)
        return await self.session.scalar(stmt)

    async def get_list_arrival_details_for_transfer(self, arrival_id: int) -> Sequence[model]:
        stmt = (select(self.model)
                .options(joinedload(self.model.part)
                         .joinedload(CatalogPart.margin))
                .where(self.model.arrive_id == arrival_id))
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_arrival_details(self, arr_detail_model: model):
        self.session.add(arr_detail_model)
        await self.session.commit()

    async def get_arrive_detail(self, arr_detail_id: int) -> model | None:
        return await self.get_one(id=arr_detail_id)

    async def delete_arrive_detail(self, arrive_detail_model: model):
        await self.session.delete(arrive_detail_model)
        await self.session.commit()
