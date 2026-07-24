from uuid import UUID

from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import UserRolesModel
from dataclasses import dataclass
from sqlalchemy import func, select
from src.application.errors import NotFoundError
from src.application.schemas.user_role import UserRoleSchema

@dataclass(slots=True, kw_only=True)
class GetUserRoleGate(PostgresGateway):
    async  def __call__(self, user_id:UUID, role: str) -> UserRoleSchema:
        stmt = (
            select(
                UserRolesModel.id,
                UserRolesModel.user_id,
                UserRolesModel.role,
                UserRolesModel.created_at,
                UserRolesModel.updated_at,
            )
            .where(UserRolesModel.user_id == user_id, UserRolesModel.role == role)
        )

        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise  NotFoundError(UserRolesModel)
        return UserRoleSchema.model_validate(result)