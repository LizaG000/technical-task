from dataclasses import dataclass
from uuid import UUID
from redis.asyncio import Redis

@dataclass(slots=True, frozen=True, kw_only=True)
class GetJWTToRedis():
    redis: Redis
    async def __call__(self, jti: UUID) -> bool:
        data = await self.redis.get(name=str(jti))
        if data is None:
            return False
        return True
        