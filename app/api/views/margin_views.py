from fastapi import APIRouter, Depends

from app.services import MarginService
from app.schemas import Margin
from app.api.dependencies import check_role_dep


margin_router = APIRouter(prefix='/margins', tags=['Наценки'], dependencies=[check_role_dep])


@margin_router.get("/all",
                   summary='Получить все категории наценок')
async def get_all_margins(margin_service: MarginService = Depends(MarginService)) -> list[Margin]:
    return await margin_service.get_all_category()


@margin_router.patch("/edit",
                     summary='Изменить категорию наценки')
async def edit_margin_category(margin: Margin, margin_service: MarginService = Depends(MarginService)) -> Margin:
    return await margin_service.edit_margin_value(margin)
