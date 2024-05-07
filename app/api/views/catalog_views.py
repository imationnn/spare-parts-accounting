from fastapi import APIRouter, Depends

from app.services import CatalogService
from app.schemas import (CatalogOutById,
                         CatalogOutByNumber,
                         CatalogUpdIn,
                         CatalogUpdOut,
                         CatalogIn,
                         CatalogInOut,
                         CatalogDelete)
from app.api.dependencies import token_dep


catalog_router = APIRouter(prefix='/catalog', tags=['Каталог деталей'], dependencies=[token_dep])


@catalog_router.get(
    "/by-id",
    summary='Получить деталь по id'
)
async def get_part_by_id(
        part_id: int,
        catalog_service: CatalogService = Depends(CatalogService)
) -> CatalogOutById:
    return await catalog_service.get_one_part_by_id(part_id)


@catalog_router.get(
    "/by-number",
    summary='Получить список деталей по номеру',
    description="Может существовать несколько одинаковых номеров под разными брендами."
)
async def get_part_by_number(
        number: str,
        catalog_service: CatalogService = Depends(CatalogService)
) -> list[CatalogOutByNumber]:
    return await catalog_service.get_parts_by_number(number)


@catalog_router.post(
    "/new",
    summary='Добавить новую деталь',
    status_code=201,
    description="Номер детали у одного бренда должен быть уникальным."
)
async def add_part(
        part: CatalogIn,
        catalog_service: CatalogService = Depends(CatalogService)
) -> CatalogInOut:
    return await catalog_service.add_part(part)


@catalog_router.put(
    "/{part_id}/edit",
    summary='Изменить информацию о детали',
    description="Нельзя изменить информацию если это приведет к дублированию существующей детали."
)
async def edit_part(
        part_id: int,
        part: CatalogUpdIn,
        catalog_service: CatalogService = Depends(CatalogService)
) -> CatalogUpdOut:
    return await catalog_service.update_part(part_id, part)


@catalog_router.delete(
    "/{part_id}/delete",
    summary='Удалить деталь',
    description="Удалить деталь можно если по ней не было поступлений."
)
async def delete_part(
        part_id: int,
        catalog_service: CatalogService = Depends(CatalogService)
) -> CatalogDelete:
    return await catalog_service.delete_part(part_id)
