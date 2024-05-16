from datetime import datetime, timedelta

from fastapi import Depends
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
    NewArrivalUpdateOut,
    NewArrivalDetailUpdateIn,
    NewArrivalDetailUpdateOut,
    NewArrivalDeleteOut,
    NewArrivalDetailDeleteOut
)
from app.exceptions import (
    ArrivalDateRangeExceeded,
    ArrivalNotFound,
    ArrivalBadParameters,
    ArrivalCheckAmount,
    ArrivalNothingTransfer,
    ArrivalAlreadyTransferred,
    ArrivalAlreadyExist
)
from app.services import CatalogService
from app.services.auth_service import NAME_FIELD_EMPLOYEE_ID


LIMIT_DATE_RANGE = 366
DEFAULT_DAYS_OFFSET = 30


class NewArrivalService:

    def __init__(
            self,
            new_arr_repository: NewArrivalRepository = Depends(),
            new_arr_det_repository: NewArrivalDetailRepository = Depends(),
            emp_cache_repository: EmployeeCacheRepository = Depends(),
            act_prod_repository: ActualProductRepository = Depends(),
            catalog_service: CatalogService = Depends()
    ):
        self.new_arr_repository = new_arr_repository
        self.new_arr_det_repository = new_arr_det_repository
        self.emp_cache_repository = emp_cache_repository
        self.act_prod_repository = act_prod_repository
        self.catalog_service = catalog_service

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
                raise ArrivalDateRangeExceeded(LIMIT_DATE_RANGE)
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
            raise ArrivalAlreadyExist
        return ArrivalNewOut.model_validate(result, from_attributes=True)

    async def add_new_arr_detail(self, new_arrive_det: ArrivalDetailNewIn, token_payload: dict) -> ArrivalDetailNewOut:
        employee_id = token_payload[NAME_FIELD_EMPLOYEE_ID]
        price_in = new_arrive_det.amount / new_arrive_det.qty
        try:
            result = await self.new_arr_det_repository.add_new_arrive_detail(
                part_id=new_arrive_det.part_id,
                qty=new_arrive_det.qty,
                price_in=price_in,
                amount=new_arrive_det.amount,
                employee_id=employee_id,
                ccd=new_arrive_det.ccd,
                arrive_id=new_arrive_det.arrive_id
            )
            await self.new_arr_det_repository.session.commit()
        except StatementError:
            raise ArrivalBadParameters
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
            raise ArrivalBadParameters
        return NewArrivalUpdateOut.model_validate(result, from_attributes=True)

    async def get_arrive_detail(self, arr_detail_id: int) -> NewArrivalDetailRepository.model:
        arrive_detail = await self.new_arr_det_repository.get_arrive_detail(arr_detail_id)
        if not arrive_detail:
            raise ArrivalNotFound
        return arrive_detail

    async def update_arr_detail(
            self,
            arr_detail_id: int,
            update_arr_det: NewArrivalDetailUpdateIn
    ) -> NewArrivalDetailUpdateOut:
        arrive_detail = await self.get_arrive_detail(arr_detail_id)
        await self._check_arrival(arrive_detail.arrive_id)
        if update_arr_det.part_id:
            arrive_detail.part_id = update_arr_det.part_id
        if update_arr_det.qty or update_arr_det.amount:
            if update_arr_det.qty:
                arrive_detail.qty = update_arr_det.qty
            if update_arr_det.amount:
                arrive_detail.amount = update_arr_det.amount
            arrive_detail.price_in = arrive_detail.amount / arrive_detail.qty
        if update_arr_det.ccd:
            arrive_detail.ccd = update_arr_det.ccd
        try:
            await self.new_arr_det_repository.update_arrival_details(arrive_detail)
        except StatementError:
            raise ArrivalBadParameters
        return NewArrivalDetailUpdateOut.model_validate(arrive_detail, from_attributes=True)

    async def delete_arrive(self, arrival_id: int) -> NewArrivalDeleteOut:
        arrive = await self._check_arrival(arrival_id)
        await self.new_arr_repository.delete_arrival(arrive)
        return NewArrivalDeleteOut.model_validate(arrive, from_attributes=True)

    async def delete_arr_detail(self, arr_detail_id: int) -> NewArrivalDetailDeleteOut:
        arrive_detail = await self.get_arrive_detail(arr_detail_id)
        await self._check_arrival(arrive_detail.arrive_id)
        await self.new_arr_det_repository.delete_arrive_detail(arrive_detail)
        return NewArrivalDetailDeleteOut.model_validate(arrive_detail, from_attributes=True)

    async def _check_arrival(self, arrive_id: int) -> NewArrivalRepository.model:
        arrive = await self.new_arr_repository.get_arrival_by_id(arrive_id)
        if not arrive:
            raise ArrivalNotFound
        if arrive.is_transferred:
            raise ArrivalAlreadyTransferred
        return arrive

    @staticmethod
    def _create_actual_product_model(
            arrival_detail_model: NewArrivalDetailRepository.model,
            shop_id: int
    ) -> ActualProductRepository.model:
        price_out = round(arrival_detail_model.price_in * arrival_detail_model.part.margin.margin_value)
        return ActualProductRepository.model(
            part_id=arrival_detail_model.part_id,
            arrived=arrival_detail_model.qty,
            rest=arrival_detail_model.qty,
            price=price_out,
            shop_id=shop_id,
            arrive_id=arrival_detail_model.arrive_id
        )

    async def transfer_arrive_to_warehouse(self, arrive_id: int):
        arrive = await self._check_arrival(arrive_id)
        if await self.new_arr_det_repository.get_total_amount_arrival_details(arrive_id) != arrive.total_price:
            raise ArrivalCheckAmount
        arrive_details = await self.new_arr_det_repository.get_list_arrival_details_for_transfer(arrive_id)
        if not arrive_details:
            raise ArrivalNothingTransfer
        list_models = [self._create_actual_product_model(item, arrive.shop_id) for item in arrive_details]
        await self.act_prod_repository.add_new_products(list_models)
        await self.new_arr_repository.update_arrival(arrive_id, is_transferred=True)
        await self.new_arr_repository.session.commit()

    async def cancel_transfer_arrive_to_warehouse(self):
        pass
