from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.users import GetUserByIdGate
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods
from src.application.schemas.users import UserRoleSchema
from dataclasses import dataclass
from loguru import logger

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserRoleUsecase(Usecase[UUID|None, UserRoleSchema]):
    session: AsyncSession
    auth: AuthSchema
    get_user_role: GetUserByIdGate
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    
    async def __call__(self, data: UUID|None=None) -> UserRoleSchema:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            r = await self.get_access_rights(self.auth.id, Elements.USER_ROLE.value, Methods.GET.value)
            logger.info(r)
            user = await self.get_user_role(data)
            logger.info(user)
            return user
            try:
                r = await self.get_access_rights(self.auth.id, Elements.USER_ROLE.value, Methods.GET.value)
                logger.info(r)
                user = await self.get_user_role(data)
                logger.info(user)
                return user
            except:
                await self.get_access_rights(self.auth.id, Elements.USER.value, Methods.GET.value)
                return await self.get_user_role(self.auth.id)