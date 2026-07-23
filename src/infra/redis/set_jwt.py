from dataclasses import dataclass
from uuid import UUID
from redis.asyncio import Redis

@dataclass(slots=True, frozen=True, kw_only=True)
class SetJWTToRedis():
    redis: Redis
    async def __call__(self, user_id: UUID, jti: UUID, expire: int) -> None:
        await self.redis.set(name=str(jti), value=str(user_id), ex=expire)