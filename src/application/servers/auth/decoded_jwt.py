import jwt
from src.infra.redis.get_jwt import GetJWTToRedis
from dataclasses import dataclass

from src.application.schemas.auth import AuthSchema
from src.config import AuthConfig
from src.application.errors import UnauthorizedError
from loguru import logger

@dataclass(slots=True, frozen=True, kw_only=True)
class DecodedJwt():
    config: AuthConfig
    get_jwt: GetJWTToRedis
    async def __call__(self, token: str):
        public_key = self.config.public_key_path.read_text()
        logger.info(public_key)
        payload = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=self.config.algorithm
        )
        logger.info(666)
        payload = AuthSchema.model_validate(payload)
        logger.info(77777)
        data = await self.get_jwt(payload.jti)
        logger.info(data)
        if data:
            raise UnauthorizedError()
        return AuthSchema.model_validate(payload)