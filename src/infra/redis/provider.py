from collections.abc import AsyncIterator
from typing import TypeVar, Type
from dishka import Provider, Scope, provide, provide_all
from src.config import RedisConfig
from loguru import logger
from redis.asyncio import Redis

from src.infra.redis.set_jwt import SetJWTToRedis
from src.infra.redis.get_jwt import GetJWTToRedis


class RedisProvider(Provider):

    @provide(scope=Scope.APP)
    async def _get_engine(self, config: RedisConfig) -> AsyncIterator[Redis]:
        client = Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            password=config.password,
            decode_responses=True,
        )

        try:
            await client.ping()
            yield client
        except:
            await client.aclose()
    
    
    _get_redis = provide_all(
        SetJWTToRedis,
        GetJWTToRedis,
    )