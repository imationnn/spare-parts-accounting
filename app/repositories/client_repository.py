from typing import Sequence

from sqlalchemy import select, or_, func, desc, and_
from sqlalchemy.orm import joinedload

from app.models import PhysicalClient, JuridicalClient
from app.repositories import BaseRepository


class PhysicalClientRepository(BaseRepository):
    model = PhysicalClient

    async def add_new_client(self, **data) -> model:
        return await self.add_one(**data)

    async def get_client_by_id(self, client_id: int) -> model | None:
        return await self.get_one(id=client_id)

    async def get_client_by_card_number(self, card_number: str) -> model | None:
        return await self.get_one(sale_card=card_number)

    async def search_client(self, search_words: list[str], limit: int = 50) -> Sequence[model]:
        stmt = (select(self.model).limit(limit))
        if len(search_words) == 1:
            word = search_words[0]
            stmt = (stmt.where(
                or_(
                    self.model.last_name.startswith(word),
                    self.model.first_name.startswith(word)
                ))).order_by(
                desc(
                    func.ts_rank(
                        func.to_tsvector(self.model.last_name),
                        func.to_tsquery(func.concat(word, ':*'))
                    )
                ))
        else:
            first_word = search_words[0]
            second_word = search_words[1]
            stmt = stmt.where(
                and_(
                    or_(self.model.last_name == first_word,
                        self.model.first_name == first_word),
                    or_(self.model.last_name.startswith(second_word),
                        self.model.first_name.startswith(second_word))
                ))
            if len(search_words) > 2:
                stmt = stmt.where(and_(self.model.patronymic.startswith(search_words[2])))
        result = await self.session.scalars(stmt)
        return result.all()


class JuridicalClientRepository(BaseRepository):
    model = JuridicalClient

    async def add_new_client(self, **data) -> model:
        return await self.add_one(**data)
