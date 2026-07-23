from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.infra.postgres.gateways.base import GetByIdGate
from src.infra.postgres.tables import UserModel
from src.infra.postgres.gateways.users import GetUserGate
from src.application.schemas.users import UserSchema
from src.usecase.auth.schemas import RequestLoginSchema, ResponseRegistrationSchema
from src.infra.postgres.tables import PasswordsModel
from dataclasses import dataclass
from src.application.errors import UnauthorizedError

@dataclass(slots=True, frozen=True, kw_only=True)
class CheckIsActive():
    session: AsyncSession
    get_user: GetByIdGate[UserModel, UUID, UserSchema]
    
    async def __call__(self, user_id: UUID) -> None:
        user = await self.get_user(user_id)
        if not user.is_active:
            raise UnauthorizedError()
            
            
            
