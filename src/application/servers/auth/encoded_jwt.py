import jwt
import uuid
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from src.config import AuthConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class EncodedJwt():
    config: AuthConfig
    async def __call__(self, user_id: uuid.UUID, role: str):
        iat = datetime.now(timezone.utc)
        expire = iat + timedelta(minutes=self.config.time)

        payload = {
            "sub": str(user_id),
            "role": role,
            "iss": "api.technical-task",
            "jti": str(uuid.uuid4()),
            "iat": int(iat.timestamp()),
            "expire": int(expire.timestamp()),
        }
        private_key = self.config.private_key_path.read_text()
        token = jwt.encode(
            payload=payload,
            key=private_key,
            algorithm="RS256"
        )
        return token