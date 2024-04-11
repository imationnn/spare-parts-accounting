from fastapi import APIRouter, Depends

from app.services import CatalogService, AuthHelper
from app.schemas import CatalogOutById, CatalogOutByNumber, CatalogUpdIn, CatalogUpdOut, CatalogIn, CatalogInOut

catalog_router = APIRouter(prefix='/catalog', tags=['Каталог деталей'], dependencies=[Depends(AuthHelper().authorize)])


@catalog_router.get("/by-id",
                    summary='Получить деталь по id')
async def get_part_by_id(part_id: int, catalog_service: CatalogService = Depends(CatalogService)) -> CatalogOutById:
    return await catalog_service.get_one_part_by_id(part_id)


@catalog_router.get("/by-number",
                    summary='Получить список деталей по номеру')
async def get_part_by_number(number: str,
                             catalog_service: CatalogService = Depends(CatalogService)) -> list[CatalogOutByNumber]:
    return await catalog_service.get_parts_by_number(number)


@catalog_router.post("/new",
                     summary='Добавить новую деталь',
                     status_code=201)
async def add_part(part: CatalogIn,
                   catalog_service: CatalogService = Depends(CatalogService)) -> CatalogInOut:
    return await catalog_service.add_part(part)


@catalog_router.put("/{part_id}/edit",
                    summary='Изменить информацию о детали')
async def edit_part(part_id: int,
                    part: CatalogUpdIn,
                    catalog_service: CatalogService = Depends(CatalogService)) -> CatalogUpdOut:
    return await catalog_service.update_part(part_id, part)
