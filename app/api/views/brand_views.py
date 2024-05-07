from fastapi import APIRouter, Depends

from app.services import BrandService
from app.schemas import BrandUpdIn, BrandId, BrandName, BrandNewIn, BrandNewOut, BrandUpdOut, BrandDelete
from app.api.dependencies import token_dep


brand_router = APIRouter(prefix='/brands', tags=['Бренды'], dependencies=[token_dep])


@brand_router.get(
    "/by-name",
    summary='Получить id бренда по названию'
)
async def get_brand_by_name(brand_name: str, brand_service: BrandService = Depends(BrandService)) -> BrandId:
    return await brand_service.get_brand_by_name(brand_name)


@brand_router.get(
    "/by-id",
    summary='Получить название бренда по id'
)
async def get_brand_by_id(brand_id: int, brand_service: BrandService = Depends(BrandService)) -> BrandName:
    return await brand_service.get_brand_by_id(brand_id)


@brand_router.post(
    "/new",
    status_code=201,
    summary='Добавить новый бренд',
    response_description="Created",
    description="Добавить бренд можно только если он не был ранее добавлен"
)
async def add_new_brand(brand_name: BrandNewIn, brand_service: BrandService = Depends(BrandService)) -> BrandNewOut:
    return await brand_service.add_brand(brand_name)


@brand_router.patch(
    "/edit",
    summary='Изменить название бренда',
    description="Изменить название можно только если такого бренда нет в списке"
)
async def edit_brand(brand: BrandUpdIn, brand_service: BrandService = Depends(BrandService)) -> BrandUpdOut:
    return await brand_service.edit_brand(brand)


@brand_router.delete(
    "/{part_id}/delete",
    summary='Удалить бренд',
    description="Удалить бренд можно только если он еще не связан ни с какой деталью"
)
async def delete_brand(brand_id: int, brand_service: BrandService = Depends(BrandService)) -> BrandDelete:
    return await brand_service.delete_brand(brand_id)
