from fastapi import Depends, HTTPException
from sqlalchemy.exc import StatementError

from app.repositories import PhysicalClientRepository, JuridicalClientRepository, OrganizationAttrRepository
from app.schemas import PhysicalClientIn, PhysicalClientOut, JuridicalClientIn, JuridicalClientOut


class ClientService:
    def __init__(
            self,
            physic_client_repository: PhysicalClientRepository = Depends(),
            jur_client_repository: JuridicalClientRepository = Depends(),
            org_attr_repository: OrganizationAttrRepository = Depends()
    ):
        self.physic_client_repository = physic_client_repository
        self.jur_client_repository = jur_client_repository
        self.org_attr_repository = org_attr_repository

    # For physic clients

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

    async def search_client(self, phrase: str) -> list[PhysicalClientOut]:
        list_words = [word for word in phrase.title().split(" ") if word]
        if not list_words:
            raise HTTPException(400, detail="Empty request")
        clients = await self.physic_client_repository.search_client(list_words)
        return [PhysicalClientOut.model_validate(client, from_attributes=True) for client in clients]

    # For juridical clients

    async def add_juridical_client(self, client: JuridicalClientIn) -> JuridicalClientOut:
        attr_model = await self.org_attr_repository.add_organization_attrs(
            **client.org_attr.model_dump(exclude_none=True)
        )
        try:
            client_model = await self.jur_client_repository.add_new_client(
                **client.model_dump(exclude_none=True, exclude={'org_attr'}),
                org_attr_id=attr_model.id
            )
        except StatementError:
            raise HTTPException(400, detail="This card number already added")
        client_model.org_attr = attr_model
        await self.jur_client_repository.session.commit()
        return JuridicalClientOut.model_validate(client_model, from_attributes=True)

    async def get_juridical_client_by_id(self, client_id: int) -> JuridicalClientOut:
        client = await self.jur_client_repository.get_client_by_id(client_id)
        if client:
            return JuridicalClientOut.model_validate(client, from_attributes=True)
        raise HTTPException(404, detail="Client not found")
