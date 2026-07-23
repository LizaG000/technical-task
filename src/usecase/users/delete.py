from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.users import SoftDeleteUserSchema
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateGate
from src.infra.postgres.tables import UserModel
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteUserUsecase(Usecase[None, None]):
    session: AsyncSession
    auth: AuthSchema
    update_user: UpdateGate[UserModel, SoftDeleteUserSchema, UUID]
    check_is_active: CheckIsActive
    
    async def __call__(self, data: None=None) -> None:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            await self.update_user(self.auth.id, SoftDeleteUserSchema())
