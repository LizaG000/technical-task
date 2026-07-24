from uuid import UUID

from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import UserRolesModel, RoleElementsModel
from dataclasses import dataclass
from src.application.schemas.permission import PermissionSchema
from sqlalchemy import func, select
from src.application.errors import ForbiddenError, NotFoundError
from loguru import logger

@dataclass(slots=True, kw_only=True)
class GetAccessRightsGate(PostgresGateway):
    async  def __call__(self, user_id: UUID, element: str, method: str) -> PermissionSchema:
        stmt = (
            select(
                RoleElementsModel.id,
                UserRolesModel.role,
                RoleElementsModel.element,
                RoleElementsModel.create,
                RoleElementsModel.patch,
                RoleElementsModel.get,
                RoleElementsModel.get_all,
                RoleElementsModel.delete,
                RoleElementsModel.created_at,
                RoleElementsModel.updated_at,
            )
            .join(UserRolesModel, UserRolesModel.role == RoleElementsModel.role)
            .where(user_id==UserRolesModel.user_id, element==RoleElementsModel.element)
        )
        match method:
            case "create":
                stmt = stmt.where(RoleElementsModel.create.is_(True))
            case "patch":
                stmt = stmt.where(RoleElementsModel.patch.is_(True))
            case "get":
                stmt = stmt.where(RoleElementsModel.get.is_(True))
            case "get_all":
                stmt = stmt.where(RoleElementsModel.get_all.is_(True))
            case "delete":
                stmt = stmt.where(RoleElementsModel.delete.is_(True))
            case _:
                raise NotFoundError(RoleElementsModel)

        

        logger.info(stmt)
        result = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(result)
        if result is None:
            raise  ForbiddenError()
        return PermissionSchema.model_validate(result)