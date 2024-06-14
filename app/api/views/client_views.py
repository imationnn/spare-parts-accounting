from fastapi import APIRouter, Depends, Query

from app.services import ClientService
from app.api.dependencies import token_dep
from app.schemas import PhysicalClientIn, PhysicalClientOut


client_router = APIRouter(prefix='/client', tags=['Клиенты'], dependencies=[token_dep])


@client_router.post(
    "/physic/new",
    summary="Добавить нового клиента"
)
async def new_physic_client(
        client: PhysicalClientIn,
        client_service: ClientService = Depends()
) -> PhysicalClientOut:
    return await client_service.add_physic_client(client)


@client_router.get(
    "/physic/by-id",
    summary="Получить клиента по id"
)
async def get_physic_client_by_id(
        client_id: int,
        client_service: ClientService = Depends()
) -> PhysicalClientOut:
    return await client_service.get_physic_client_by_id(client_id)


@client_router.get(
    "/physic/by-card-number",
    summary="Получить клиента по номеру карты"
)
async def get_physic_client_by_card_number(
        card_number: str,
        client_service: ClientService = Depends()
) -> PhysicalClientOut:
    return await client_service.get_physic_client_by_card_number(card_number)


@client_router.get(
    "/physic/search",
    summary="Найти клиента",
    description="Слова в фразе должны быть разделены пробелом, первые буквы в словах не обязательно должны быть заглавными."
                "Если слово одно то результат сортируется по фамилиям соответствующим данному слову."
                "Если слов 2 или 3 то первое используется для точного поиска."
                "Например Иванов А А, будут варианты с фамилией Иванов и всеми именами и отчествами на А."
                "Иван А А, будут все варианты с именем Иван и фамилиями и отчествами на А."
)
async def search_physic_client(
        phrase: str = Query(min_length=2),
        client_service: ClientService = Depends()
) -> list[PhysicalClientOut]:
    return await client_service.search_client(phrase)
