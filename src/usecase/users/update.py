from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.users import UserSchema, UpdateUserSchema
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import UserModel
from src.application.schemas.auth import AuthSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserUsecase(Usecase[UpdateUserSchema, None]):
    session: AsyncSession
    auth: AuthSchema
    update_user: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchema]
    
    async def __call__(self, data: UpdateUserSchema) -> None:
        async with self.session.begin():
            return await self.update_user(self.auth.id, data)
