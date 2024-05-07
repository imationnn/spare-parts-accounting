from fastapi import APIRouter

from .views import (
    brand_router,
    margin_router,
    catalog_router,
    auth_router,
    employee_router,
    shop_router,
    supplier_router,
    arrive_router)


main_router = APIRouter()
main_router.include_router(brand_router)
main_router.include_router(margin_router)
main_router.include_router(catalog_router)
main_router.include_router(auth_router)
main_router.include_router(employee_router)
main_router.include_router(shop_router)
main_router.include_router(supplier_router)
main_router.include_router(arrive_router)
