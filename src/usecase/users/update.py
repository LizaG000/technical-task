from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.users import UserSchema, UpdateUserSchema
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import UserModel
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods
from dataclasses import dataclass
from loguru import logger

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserUsecase(Usecase[UpdateUserSchema, UserSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_user: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchema]
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    
    async def __call__(self, data: UpdateUserSchema) -> UserSchema:
        async with self.session.begin():
            logger.info(1)
            await self.check_is_active(self.auth.id)
            logger.info(2)
            await self.get_access_rights(self.auth.id, Elements.USER.value, Methods.PATCH.value)
            logger.info(3)
            return await self.update_user(self.auth.id, data)
