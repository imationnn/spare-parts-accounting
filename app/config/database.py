from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis

from .config import PGConfig, RedisConfig


class PGDatabase:
    def __init__(self, pg_config: PGConfig = PGConfig()):
        self.pg_config = pg_config
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


class RedisDatabase:
    def __init__(self, redis_config: RedisConfig = RedisConfig()):
        self.config = redis_config
        self.redis = Redis(host=self.config.redis_host,
                           port=self.config.redis_port,
                           db=self.config.redis_db_name,
                           password=self.config.redis_password)

    def __call__(self, *args, **kwargs):
        return self.redis


db_connector = PGDatabase()
redis_db = RedisDatabase()
