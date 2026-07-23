from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.gateways.user_roles import GetUserRoleGate
from src.application.schemas.users import SoftDeleteUserSchema
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.tables import UserRolesModel
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods
from src.application.schemas.user_role import CreateUserRoleSchema, UserRoleSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserRoleUsecase(Usecase[CreateUserRoleSchema, UserRoleSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_user_role: CreateReturningGate[UserRolesModel, CreateUserRoleSchema, UserRoleSchema]
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    get_user_role: GetUserRoleGate
    
    async def __call__(self, data: CreateUserRoleSchema) -> UserRoleSchema:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            await self.get_access_rights(self.auth.id, Elements.USER_ROLE.value, Methods.CREATE.value)
            try:
                return await self.get_user_role(data.user_id, data.role)
            except:
                return await self.create_user_role(data)


