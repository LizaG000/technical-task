from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.users import UserSchema, UpdateUserSchema
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import UserModel
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserUsecase(Usecase[UpdateUserSchema, UserSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_user: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchema]
    check_is_active: CheckIsActive
    
    async def __call__(self, data: UpdateUserSchema) -> UserSchema:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            return await self.update_user(self.auth.id, data)
