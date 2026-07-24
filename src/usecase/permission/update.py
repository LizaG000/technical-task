from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import RoleElementsModel
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods
from dataclasses import dataclass
from src.usecase.permission.schemas import RequestUpdateRoleElementSchema
from src.application.schemas.permission import PermissionSchema, UpdatePermissionSchema

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdatePermissionUsecase(Usecase[RequestUpdateRoleElementSchema, PermissionSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_permission: UpdateReturningGate[RoleElementsModel, UpdatePermissionSchema, UUID, PermissionSchema]
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    
    async def __call__(self, data: RequestUpdateRoleElementSchema) -> PermissionSchema:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            await self.get_access_rights(self.auth.id, Elements.PERMISSION.value, Methods.PATCH.value)
            return await self.update_permission(data.id, data.data)
