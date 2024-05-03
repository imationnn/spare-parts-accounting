from fastapi import APIRouter, Depends

from app.services import SupplierService
from app.schemas import SupplierOut, SupplierIn, SupplierListOut, SupplierUpdate
from app.api.dependencies import token_dep


supplier_router = APIRouter(prefix='/supplier', tags=['Поставщики'], dependencies=[token_dep])


@supplier_router.get("/by-id",
                     summary='Получить информацию о поставщике по id')
async def get_supplier_by_id(
        supplier_id: int,
        supplier_service: SupplierService = Depends(SupplierService)
) -> SupplierOut:
    return await supplier_service.get_supplier_by_id(supplier_id)


@supplier_router.get("/all",
                     summary='Получить всех поставщиков')
async def get_all_suppliers(
        limit: int = 500,
        offset: int = 0,
        supplier_service: SupplierService = Depends(SupplierService)
) -> list[SupplierListOut]:
    return await supplier_service.get_all_suppliers(limit, offset)


@supplier_router.post("/new",
                      summary='Добавить поставщика')
async def add_new_supplier(
        supplier: SupplierIn,
        supplier_service: SupplierService = Depends(SupplierService)
) -> SupplierOut:
    return await supplier_service.add_new_supplier(supplier)


@supplier_router.patch("/update",
                       summary='Обновить информацию о поставщике')
async def update_supplier(
        supplier_id: int,
        supplier: SupplierUpdate,
        supplier_service: SupplierService = Depends(SupplierService)
) -> SupplierOut:
    return await supplier_service.update_supplier(supplier_id, supplier)
