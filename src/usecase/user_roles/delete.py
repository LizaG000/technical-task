from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.infra.postgres.gateways.user_roles import DeleteUserRoleGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods
from src.application.schemas.user_role import DeleteUserRoleSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteUserRoleUsecase(Usecase[None, None]):
    session: AsyncSession
    auth: AuthSchema
    delete_user_role: DeleteUserRoleGate
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    
    async def __call__(self, data: DeleteUserRoleSchema) -> None:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            await self.get_access_rights(self.auth.id, Elements.USER_ROLE.value, Methods.DELETE.value)
            await self.delete_user_role(data.user_id, data.role)
