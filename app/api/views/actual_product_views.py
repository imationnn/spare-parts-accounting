from fastapi import APIRouter, Depends, Body

from app.services import ActualProductService
from app.api.dependencies import token_dep
from app.schemas import ActualProductOutById, ActualProductOutByPartId

act_product_router = APIRouter(prefix='/actual', tags=['Товары в наличии'], dependencies=[token_dep])


@act_product_router.get(
    "/product-by-id",
    summary="Получить информацию о товаре в наличии по id"
)
async def get_product_by_id(
        product_id: int,
        act_product_service: ActualProductService = Depends()
) -> ActualProductOutById:
    return await act_product_service.get_actual_product_by_id(product_id)


@act_product_router.post(
    "/product-by-list-parts-id",
    summary="Получить список товаров по списку parts id"
)
async def get_list_actual_products(
        parts_id_list: list[int] = Body(description="Список part id"),
        act_product_service: ActualProductService = Depends()
) -> list[ActualProductOutByPartId]:
    return await act_product_service.get_list_actual_products_by_part_id(parts_id_list)
