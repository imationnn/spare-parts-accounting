from fastapi import APIRouter

from .views import brand_router


main_router = APIRouter()
main_router.include_router(brand_router)
