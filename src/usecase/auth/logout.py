from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.usecase.base import Usecase
from src.infra.redis.set_jwt import SetJWTToRedis
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class LogoutUserUsecase(Usecase[None, None]):
    session: AsyncSession
    auth: AuthSchema
    check_is_active: CheckIsActive
    set_jwt: SetJWTToRedis
    
    async def __call__(self, data: None=None) -> None:
        async with self.session.begin():
            self.check_is_active(self.auth.id)
            now = datetime.now(timezone.utc)
            expire = self.auth.expire - int(now.timestamp())
            await self.set_jwt(self.auth.id, self.auth.jti, expire)

            
            
