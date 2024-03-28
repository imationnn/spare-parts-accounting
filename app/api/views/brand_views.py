from fastapi import APIRouter, Depends

from app.services import BrandService
from app.schemas import BrandUpdIn, BrandId, BrandName, BrandNewIn, BrandNewOut, BrandUpdOut


brand_router = APIRouter(prefix='/brands', tags=['Бренды'])


@brand_router.get("/by-name",
                  summary='Получить id бренда по названию')
async def get_brand_by_name(brand_name: str, brand_service: BrandService = Depends(BrandService)) -> BrandId:
    return await brand_service.get_brand_by_name(brand_name)


@brand_router.get("/by-id",
                  summary='Получить название бренда по id')
async def get_brand_by_id(brand_id: int, brand_service: BrandService = Depends(BrandService)) -> BrandName:
    return await brand_service.get_brand_by_id(brand_id)


@brand_router.post("/new",
                   status_code=201,
                   summary='Добавить новый бренд',
                   response_description="Created")
async def add_new_brand(brand_name: BrandNewIn, brand_service: BrandService = Depends(BrandService)) -> BrandNewOut:
    return await brand_service.add_brand(brand_name)


@brand_router.patch("/edit",
                    summary='Изменить название бренда')
async def edit_brand(brand: BrandUpdIn, brand_service: BrandService = Depends(BrandService)) -> BrandUpdOut:
    return await brand_service.edit_brand(brand)
