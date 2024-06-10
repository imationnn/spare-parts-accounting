from fastapi import Depends, HTTPException
from sqlalchemy.exc import StatementError

from app.repositories import PhysicalClientRepository, JuridicalClientRepository
from app.schemas import PhysicalClientIn, PhysicalClientOut


class ClientService:
    def __init__(
            self,
            physic_client_repository: PhysicalClientRepository = Depends(),
            jur_client_repository: JuridicalClientRepository = Depends()
    ):
        self.physic_client_repository = physic_client_repository
        self.jur_client_repository = jur_client_repository

    async def add_physic_client(self, client: PhysicalClientIn) -> PhysicalClientOut:
        try:
            result = await self.physic_client_repository.add_new_client(**client.model_dump())
            await self.physic_client_repository.session.commit()
            return PhysicalClientOut.model_validate(result, from_attributes=True)
        except StatementError:
            raise HTTPException(400, detail="This card number already added")

    async def get_physic_client_by_id(self, client_id: int) -> PhysicalClientOut:
        client = await self.physic_client_repository.get_client_by_id(client_id)
        if client:
            return PhysicalClientOut.model_validate(client, from_attributes=True)
        raise HTTPException(404, detail="Client not found")

    async def get_physic_client_by_card_number(self, card_number: str) -> PhysicalClientOut:
        client = await self.physic_client_repository.get_client_by_card_number(card_number)
        if client:
            return PhysicalClientOut.model_validate(client, from_attributes=True)
        raise HTTPException(404, detail="Client not found")
