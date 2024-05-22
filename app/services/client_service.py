from fastapi import Depends

from app.repositories import PhysicalClientRepository, JuridicalClientRepository


class ClientService:
    def __init__(
            self,
            physic_client_repository: PhysicalClientRepository = Depends(),
            jur_client_repository: JuridicalClientRepository = Depends()
    ):
        self.physic_client_repository = physic_client_repository
        self.jur_client_repository = jur_client_repository
