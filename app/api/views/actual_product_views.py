from datetime import datetime

from fastapi import APIRouter, Depends, Body, Query

from app.services import ActualProductService
from app.services.actual_product_service import LIMIT_DATE_RANGE
from app.api.dependencies import token_dep
from app.schemas import ActualProductOutById, ActualProductOutByPartId

act_product_router = APIRouter(prefix='/actual', tags=['Товары в наличии'], dependencies=[token_dep])


class DescriptionQueryActualProducts:
    parts_id_list = "Список part id"
    show_archive = "Показать архив товаров"
    from_date = f"С какой даты показать архив. По умолчанию {LIMIT_DATE_RANGE} дней с текущего времени"
    to_date = "По какую дату показать архив. По умолчанию по текущее время"
    only_current_shop = "Товары только для текущего магазина"


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
    summary="Получить список товаров по списку parts id",
    description=f"Максимальный диапазон дат для архива {LIMIT_DATE_RANGE} дней"
)
async def get_list_actual_products(
        parts_id_list: list[int] = Body(description=DescriptionQueryActualProducts.parts_id_list),
        show_archive: bool = Query(default=False, description=DescriptionQueryActualProducts.show_archive),
        from_date: datetime = Query(default=None, description=DescriptionQueryActualProducts.from_date),
        to_date: datetime = Query(default=None, description=DescriptionQueryActualProducts.to_date),
        only_current_shop: bool = Query(default=False, description=DescriptionQueryActualProducts.only_current_shop),
        act_product_service: ActualProductService = Depends(),
        token_payload: dict = token_dep
) -> list[ActualProductOutByPartId]:
    return await act_product_service.get_list_actual_products_by_part_id(
        parts_id_list=parts_id_list,
        token_payload=token_payload,
        archive=show_archive,
        from_date=from_date,
        to_date=to_date,
        only_current_shop=only_current_shop
    )
