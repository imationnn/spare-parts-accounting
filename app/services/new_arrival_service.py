from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.exc import StatementError

from app.repositories import (
    NewArrivalRepository,
    NewArrivalDetailRepository,
    EmployeeCacheRepository,
    ActualProductRepository
)
from app.schemas import (
    NewArrivalOut,
    NewArrivalIn,
    ArrivalNewOut,
    ArrivalDetailNewIn,
    ArrivalDetailNewOut,
    NewArrivalDetailGetList,
    NewArrivalUpdateIn,
    NewArrivalUpdateOut
)
from app.services.auth_service import NAME_FIELD_EMPLOYEE_ID


LIMIT_DATE_RANGE = 366
DEFAULT_DAYS_OFFSET = 30


class NewArrivalService:

    def __init__(
            self,
            new_arr_repository: NewArrivalRepository = Depends(),
            new_arr_det_repository: NewArrivalDetailRepository = Depends(),
            emp_cache_repository: EmployeeCacheRepository = Depends(),
            act_prod_repository: ActualProductRepository = Depends()
    ):
        self.new_arr_repository = new_arr_repository
        self.new_arr_det_repository = new_arr_det_repository
        self.emp_cache_repository = emp_cache_repository
        self.act_prod_repository = act_prod_repository

    async def get_arrivals(
            self,
            from_date: datetime | None,
            to_date: datetime | None,
            is_transferred: bool | None,
            sort_by: str,
            limit: int,
            offset: int,
            token_payload: dict
    ) -> list[NewArrivalOut]:
        if from_date:
            if to_date is None:
                to_date = datetime.now()
            if (to_date - from_date) > timedelta(days=LIMIT_DATE_RANGE):
                raise HTTPException(400)
        else:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=DEFAULT_DAYS_OFFSET)

        emp_cache = await self.emp_cache_repository.get_employee_cache(token_payload[NAME_FIELD_EMPLOYEE_ID])
        result = await self.new_arr_repository.get_arrivals(
            from_date=from_date,
            to_date=to_date,
            shop_id=emp_cache.shop_id,
            is_transferred=is_transferred,
            sort_by=sort_by,
            limit=limit,
            offset=offset
        )
        return [NewArrivalOut.model_validate(item, from_attributes=True) for item in result]

    async def get_arr_details_by_arrive_id(self, arrive_id: int) -> list[NewArrivalDetailGetList]:
        result = await self.new_arr_det_repository.get_list_arrival_details(arrive_id)
        return [NewArrivalDetailGetList.model_validate(item, from_attributes=True) for item in result]

    async def create_new_arrive(self, new_arrive: NewArrivalIn, token_payload: dict) -> ArrivalNewOut:
        employee_id = token_payload[NAME_FIELD_EMPLOYEE_ID]
        emp_cache = await self.emp_cache_repository.get_employee_cache(employee_id)
        try:
            result = await self.new_arr_repository.create_new_arrival(
                emp_cache.shop_id,
                employee_id,
                new_arrive.model_dump()
            )
            await self.new_arr_repository.session.commit()
        except StatementError:
            raise HTTPException(400)
        return ArrivalNewOut.model_validate(result, from_attributes=True)

    async def add_new_arr_detail(self, new_arrive_det: ArrivalDetailNewIn, token_payload: dict) -> ArrivalDetailNewOut:
        employee_id = token_payload[NAME_FIELD_EMPLOYEE_ID]
        price_in = new_arrive_det.amount / new_arrive_det.qty
        price_out = round(price_in * new_arrive_det.part.margin_value)
        try:
            result = await self.new_arr_det_repository.add_new_arrive_detail(
                part_id=new_arrive_det.part.part_id,
                qty=new_arrive_det.qty,
                price_in=price_in,
                price_out=price_out,
                amount=new_arrive_det.amount,
                employee_id=employee_id,
                ccd=new_arrive_det.ccd,
                arrive_id=new_arrive_det.arrive_id
            )
            await self.new_arr_det_repository.session.commit()
        except StatementError:
            raise HTTPException(400)
        return ArrivalDetailNewOut.model_validate(result, from_attributes=True)

    async def update_arrive(self, arrive_id: int, update_arrival: NewArrivalUpdateIn) -> NewArrivalUpdateOut:
        await self._check_arrival(arrive_id)
        try:
            result = await self.new_arr_repository.update_arrival(
                arrive_id,
                **update_arrival.model_dump(exclude_unset=True)
            )
            await self.new_arr_repository.session.commit()
        except StatementError:
            raise HTTPException(400)
        return NewArrivalUpdateOut.model_validate(result, from_attributes=True)

    async def update_arr_detail(self):
        pass

    async def delete_arrive(self):
        pass

    async def delete_arr_detail(self):
        pass

    async def _check_arrival(self, arrive_id: int) -> NewArrivalRepository.model:
        arrive = await self.new_arr_repository.get_arrival_by_id(arrive_id)
        if not arrive:
            raise HTTPException(404, "Arrival does not exist")
        if arrive.is_transferred:
            raise HTTPException(400, "Arrival already transferred")
        return arrive

    async def transfer_arrive_to_warehouse(self, arrive_id: int):
        arrive = await self._check_arrival(arrive_id)
        if await self.new_arr_det_repository.get_total_amount_arrival_details(arrive_id) != arrive.total_price:
            raise HTTPException(400, "Check the amount")
        arrive_details = await self.new_arr_det_repository.get_list_arrival_details_for_transfer(arrive_id)
        if not arrive_details:
            raise HTTPException(400, "Nothing to transfer")
        list_models = [self.act_prod_repository.model(
            part_id=item.part_id,
            arrived=item.qty,
            rest=item.qty,
            price=item.price_out,
            shop_id=arrive.shop_id,
            arrive_id=arrive_id
        ) for item in arrive_details]
        await self.act_prod_repository.add_new_products(list_models)
        await self.new_arr_repository.update_arrival(arrive_id, is_transferred=True)
        await self.new_arr_repository.session.commit()

    async def cancel_transfer_arrive_to_warehouse(self):
        pass
