from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.exc import StatementError

from app.repositories import NewArrivalRepository, NewArrivalDetailRepository, EmployeeCacheRepository
from app.schemas import NewArrivalOut, NewArrivalIn, ArrivalNewOut
from app.services.auth_service import NAME_FIELD_EMPLOYEE_ID


LIMIT_DATE_RANGE = 366
DEFAULT_DAYS_OFFSET = 30


class NewArrivalService:

    def __init__(
            self,
            new_arr_repository: NewArrivalRepository = Depends(),
            new_arr_det_repository: NewArrivalDetailRepository = Depends(),
            emp_cache_repository: EmployeeCacheRepository = Depends()
    ):
        self.new_arr_repository = new_arr_repository
        self.new_arr_det_repository = new_arr_det_repository
        self.emp_cache_repository = emp_cache_repository

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

    async def get_arr_details_by_arrive_id(self) -> list:
        pass

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

    async def add_new_arr_detail(self):
        pass

    async def update_arrive(self):
        pass

    async def update_arr_detail(self):
        pass

    async def delete_arrive(self):
        pass

    async def delete_arr_detail(self):
        pass

    async def transfer_arrive_to_warehouse(self):
        pass

    async def cancel_transfer_arrive_to_warehouse(self):
        pass
