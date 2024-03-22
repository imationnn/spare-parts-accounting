from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from asyncio import current_task

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

    def get_scoped_session(self):
        return async_scoped_session(session_factory=self.session_factory,
                                    scopefunc=current_task)

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = Database()
