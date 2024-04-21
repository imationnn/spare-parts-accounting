from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector
from app.repositories import BaseRepository


class BaseService:
    repository: BaseRepository

    def __init__(self, session: AsyncSession = Depends(db_connector.get_session)):
        self.repository.session = session
