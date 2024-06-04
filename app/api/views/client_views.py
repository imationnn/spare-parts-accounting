from fastapi import APIRouter, Depends

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
