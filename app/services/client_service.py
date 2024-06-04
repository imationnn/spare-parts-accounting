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
