from sqlalchemy.ext.asyncio import AsyncSession
from src.config import DataConfig
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetByIdUserGate
from src.infra.postgres.gateways.users import GetUserGate
from src.application.schemas.password import PasswordSchema
from src.usecase.auth.schemas import RequestLoginSchema, ResponseRegistrationSchema
from src.infra.postgres.tables import PasswordsModel
from dataclasses import dataclass
from src.application.servers.auth.check_password import check_password
from src.application.errors import InvalidCredentialsError
from src.application.servers.auth.encoded_jwt import EncodedJwt
from loguru import logger

@dataclass(slots=True, frozen=True, kw_only=True)
class LoginUserUsecase(Usecase[RequestLoginSchema, ResponseRegistrationSchema]):
    session: AsyncSession
    get_user: GetUserGate
    get_password: GetByIdUserGate[PasswordsModel, PasswordSchema, UUID]
    encode_jwt: EncodedJwt
    
    async def __call__(self, data: RequestLoginSchema) -> ResponseRegistrationSchema:
        async with self.session.begin():
            user = await self.get_user(data.email)
            logger.info(user)
            password = await self.get_password(user.id)
            if not check_password(data.password, password.password):
                raise InvalidCredentialsError()
            token = await self.encode_jwt(user.id, user.role)
            return ResponseRegistrationSchema(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                token=token
            )
            
            
