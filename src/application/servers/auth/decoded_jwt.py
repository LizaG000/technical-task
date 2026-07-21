import jwt
import uuid
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

from pydantic import json
from application.schemas.auth import AuthSchemas
from src.config import AuthConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class DecodedJwt():
    config: AuthConfig
    async def __call__(self, token: str):
        public_key = self.config.public_key_path.read_text()
        payload = jwt.decode(
            jwt=token,
            key=public_key,
            algorithm="RS256"
        )
        return AuthSchemas.model_validate(json.loads(payload))