from fastapi import APIRouter, Depends

from app.models import Roles
from app.services import MarginService, CheckRole
from app.schemas import Margin


margin_router = APIRouter(
    prefix='/margins',
    tags=['Наценки'],
    dependencies=[Depends(CheckRole([
        Roles.admin["id"],
        Roles.director["id"]
    ]))])


@margin_router.get("/all",
                   summary='Получить все категории наценок')
async def get_all_margins(margin_service: MarginService = Depends(MarginService)) -> list[Margin]:
    return await margin_service.get_all_category()


@margin_router.patch("/edit",
                     summary='Изменить категорию наценки')
async def edit_margin_category(margin: Margin, margin_service: MarginService = Depends(MarginService)) -> Margin:
    return await margin_service.edit_margin_value(margin)
