from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import PhysicalClient, JuridicalClient
from app.repositories import BaseRepository


class PhysicalClientRepository(BaseRepository):
    model = PhysicalClient

    async def add_new_client(self, **data) -> model:
        return await self.add_one(**data)


class JuridicalClientRepository(BaseRepository):
    model = JuridicalClient
