from typing import Literal
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.services import NewArrivalService
from app.schemas import NewArrivalOut, NewArrivalIn, ArrivalNewOut
from app.api.dependencies import token_dep
from app.services.new_arrival_service import DEFAULT_DAYS_OFFSET


arrive_router = APIRouter(prefix='/new_arrival', tags=['Новые поступления'], dependencies=[token_dep])


class DescriptionQueryArrival:
    from_date = f"С какой даты показать поступления. По умолчанию {DEFAULT_DAYS_OFFSET} дней с текущего времени"
    to_date = "По какую дату показать поступления. По умолчанию по текущее время"
    is_transferred = "Признак передачи. По умолчанию возвращаются поступления со всеми признаками."
    sort_by = "По какому полю сортировать поступления"


@arrive_router.get(
    "/list-arrivals",
    summary="Получить список новых поступлений",
    description="Максимальный диапазон между начальной и конечной датой - 366 дней"
)
async def get_list_arrivals(
        from_date: datetime = Query(default=None, description=DescriptionQueryArrival.from_date),
        to_date: datetime = Query(default=None, description=DescriptionQueryArrival.to_date),
        is_transferred: bool = Query(default=None, description=DescriptionQueryArrival.is_transferred),
        sort_by: Literal["id", "created_at"] = Query(default="id", description=DescriptionQueryArrival.sort_by),
        limit: int = Query(default=300, le=300),
        offset: int = 0,
        arrival_service: NewArrivalService = Depends(),
        token_payload: dict = token_dep
) -> list[NewArrivalOut]:
    return await arrival_service.get_arrivals(
        from_date=from_date,
        to_date=to_date,
        is_transferred=is_transferred,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
        token_payload=token_payload
    )


@arrive_router.post(
    "/create",
    summary="Создать новое поступление",
    description="Номер накладной у одного поставщика должен быть уникальным."
)
async def create_new_arrival(
        new_arrival: NewArrivalIn,
        arrival_service: NewArrivalService = Depends(),
        token_payload: dict = token_dep
) -> ArrivalNewOut:
    return await arrival_service.create_new_arrive(new_arrival, token_payload)
