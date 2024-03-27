from fastapi import APIRouter, Depends

from app.services.brand_service import BrandService
from app.schemas import BrandInUpd

brand_router = APIRouter(prefix='/brands', tags=['Бренды'])


@brand_router.get("/by_name",
                  description='Возвращает id бренда по его названию',
                  summary='Получить id бренда по названию')
async def get_brand_by_name(brand_name: str, brand_service: BrandService = Depends(BrandService)):
    return await brand_service.get_brand_by_name(brand_name)


@brand_router.get("/{brand_id}",
                  description='Возвращает название бренда по его id',
                  summary='Получить название бренда по id')
async def get_brand_by_id(brand_id: int, brand_service: BrandService = Depends(BrandService)):
    return await brand_service.get_brand_by_id(brand_id)


@brand_router.post("/add_one")
async def add_new_brand(brand_name: str, brand_service: BrandService = Depends(BrandService)):
    return await brand_service.add_brand(brand_name)


@brand_router.patch("/edit_one")
async def edit_brand(brand: BrandInUpd, brand_service: BrandService = Depends(BrandService)):
    return await brand_service.edit_brand(brand)
