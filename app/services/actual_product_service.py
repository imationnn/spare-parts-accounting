from fastapi import Depends, HTTPException

from app.repositories import ActualProductRepository, EmployeeCacheRepository
from app.schemas import ActualProductOutByPartId, ActualProductOutById


class ActualProductService:

    def __init__(
            self,
            actual_prod_repository: ActualProductRepository = Depends(),
            emp_cache_repository: EmployeeCacheRepository = Depends()
    ):
        self.actual_prod_repository = actual_prod_repository
        self.emp_cache_repository = emp_cache_repository

    async def get_actual_product_by_id(self, product_id: int) -> ActualProductOutById:
        product = await self.actual_prod_repository.get_actual_product(product_id)
        if not product:
            raise HTTPException(404, "Actual product not found")
        return ActualProductOutById.model_validate(product, from_attributes=True)

    async def get_list_actual_products_by_part_id(self, parts_id_list: list) -> list[ActualProductOutByPartId]:
        if not parts_id_list:
            return []
        res = await self.actual_prod_repository.get_list_actual_products(parts_id_list)
        return [ActualProductOutByPartId.model_validate(item, from_attributes=True) for item in res]

    async def update_actual_product(self):
        pass
