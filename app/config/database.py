from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from .config import PGConfig


class Database:
    def __init__(self):
        self.pg_config = PGConfig()
        self.engine = create_async_engine(url=self.pg_config.pg_dsn, echo=self.pg_config.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session


db_connector = Database()
