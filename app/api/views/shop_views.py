from fastapi import APIRouter, Depends

from app.services import ShopService
from app.schemas import ShopOut, ShopIn, ShopUpd
from app.api.dependencies import check_role_dep


shop_router = APIRouter(prefix='/shop', tags=['Магазины'], dependencies=[check_role_dep])


@shop_router.get("/by-id",
                 summary='Получить информацию о магазине по id')
async def get_shop_by_id(
        shop_id: int,
        shop_service: ShopService = Depends(ShopService)
) -> ShopOut:
    return await shop_service.get_shop_by_id(shop_id)


@shop_router.get("/all",
                 summary='Получить все магазины')
async def get_all_shops(shop_service: ShopService = Depends(ShopService)) -> list[ShopOut]:
    return await shop_service.get_all_shops()


@shop_router.post("/new",
                  summary='Добавить новый магазин',
                  status_code=201)
async def add_new_shop(
        shop: ShopIn,
        shop_service: ShopService = Depends(ShopService)
) -> ShopOut:
    return await shop_service.add_new_shop(shop)


@shop_router.put("/{shop_id}/edit",
                 summary='Изменить информацию о магазине')
async def update_shop(
        shop_id: int,
        shop: ShopUpd,
        shop_service: ShopService = Depends(ShopService)
) -> ShopOut:
    return await shop_service.update_shop(shop_id, shop)
