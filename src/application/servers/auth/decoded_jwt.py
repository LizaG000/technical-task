import jwt
import uuid
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

from pydantic import json
from src.application.schemas.auth import AuthSchema
from src.config import AuthConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class DecodedJwt():
    config: AuthConfig
    async def __call__(self, token: str):
        public_key = self.config.public_key_path.read_text()
        payload = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=self.config.algorithm
        )
        return AuthSchema.model_validate(payload)