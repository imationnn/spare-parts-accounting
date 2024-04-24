from fastapi import APIRouter, Depends

from app.services import SupplierService
from app.schemas import SupplierOut, SupplierIn
from app.api.dependencies import token_dep


supplier_router = APIRouter(prefix='/supplier', tags=['Поставщики'], dependencies=[token_dep])


@supplier_router.get("/by-id",
                     summary='Получить информацию о поставщике по id')
async def get_supplier_by_id(
        supplier_id: int,
        supplier_service: SupplierService = Depends(SupplierService)
) -> SupplierOut:
    return await supplier_service.get_supplier_by_id(supplier_id)


@supplier_router.post("/new",
                      summary='Добавить поставщика')
async def add_new_supplier(
        supplier: SupplierIn,
        supplier_service: SupplierService = Depends(SupplierService)
) -> SupplierOut:
    return await supplier_service.add_new_supplier(supplier)
