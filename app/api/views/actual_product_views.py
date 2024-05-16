from fastapi import APIRouter, Depends

from app.services import ActualProductService
from app.api.dependencies import token_dep
from app.schemas import ActualProductOutById


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
