import jwt
from src.infra.redis.get_jwt import GetJWTToRedis
from dataclasses import dataclass

from src.application.schemas.auth import AuthSchema
from src.config import AuthConfig
from src.application.errors import UnauthorizedError

@dataclass(slots=True, frozen=True, kw_only=True)
class DecodedJwt():
    config: AuthConfig
    get_jwt: GetJWTToRedis
    async def __call__(self, token: str):
        public_key = self.config.public_key_path.read_text()
        payload = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=self.config.algorithm
        )
        payload = AuthSchema.model_validate(payload)
        if await self.get_jwt(payload.jti):
            raise UnauthorizedError()
        return AuthSchema.model_validate(payload)