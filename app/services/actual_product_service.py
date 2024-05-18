from datetime import datetime, timedelta

from fastapi import Depends, HTTPException

from app.repositories import ActualProductRepository, EmployeeCacheRepository
from app.schemas import ActualProductOutByPartId, ActualProductOutById, ActualProductUpdateOut, ActualProductUpdateIn
from app.services.auth_service import NAME_FIELD_EMPLOYEE_ID


LIMIT_DATE_RANGE = 366


class ActualProductService:

    def __init__(
            self,
            actual_prod_repository: ActualProductRepository = Depends(),
            emp_cache_repository: EmployeeCacheRepository = Depends()
    ):
        self.actual_prod_repository = actual_prod_repository
        self.emp_cache_repository = emp_cache_repository

    async def _get_actual_product_by_id(self, product_id: int) -> ActualProductRepository.model:
        product = await self.actual_prod_repository.get_actual_product(product_id)
        if not product:
            raise HTTPException(404, "Actual product not found")
        return product

    async def get_actual_product_by_id(self, product_id: int) -> ActualProductOutById:
        return ActualProductOutById.model_validate(
            await self._get_actual_product_by_id(product_id),
            from_attributes=True
        )

    async def get_list_actual_products_by_part_id(
            self,
            parts_id_list: list,
            token_payload: dict,
            archive: bool | None,
            from_date: datetime = None,
            to_date: datetime = None,
            only_current_shop: bool = False
    ) -> list[ActualProductOutByPartId]:
        if not parts_id_list:
            return []
        if archive:
            timedelta_limit = timedelta(days=LIMIT_DATE_RANGE)
            if to_date is None:
                to_date = datetime.now()
            if from_date is None:
                from_date = to_date - timedelta_limit
            if (to_date - from_date) > timedelta_limit:
                raise HTTPException(400, f"Date range exceeded, available limit {LIMIT_DATE_RANGE} days")
            date_range = (from_date, to_date)
        else:
            date_range = None
        if only_current_shop:
            emp_cache = await self.emp_cache_repository.get_employee_cache(token_payload[NAME_FIELD_EMPLOYEE_ID])
            current_shop = emp_cache.shop_id
        else:
            current_shop = None
        result = await self.actual_prod_repository.get_list_actual_products(
            parts_id=parts_id_list,
            date_range=date_range,
            current_shop=current_shop
        )
        return [ActualProductOutByPartId.model_validate(item, from_attributes=True) for item in result]

    async def update_actual_product(
            self,
            product_id: int,
            act_prod_update: ActualProductUpdateIn
    ) -> ActualProductUpdateOut:
        values = act_prod_update.model_dump(exclude_unset=True)
        if not values:
            raise HTTPException(400)
        await self._get_actual_product_by_id(product_id)
        result = await self.actual_prod_repository.update_actual_product(product_id, **values)
        return ActualProductUpdateOut.model_validate(result, from_attributes=True)
