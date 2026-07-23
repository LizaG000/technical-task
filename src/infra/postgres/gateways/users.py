from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import UserModel, UserRolesModel
from dataclasses import dataclass
from src.application.schemas.users import UserRoleSchema
from sqlalchemy import func, select
from src.application.errors import InvalidCredentialsError

@dataclass(slots=True, kw_only=True)
class GetUserGate(PostgresGateway):
    async  def __call__(self, email: str) -> UserRoleSchema:
        stmt = (
            select(
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.middle_name,
                UserModel.email,
                UserModel.is_active,
                UserModel.created_at,
                UserModel.updated_at,
                func.array_agg(
                    UserRolesModel.role
                ).label("roles"),
            )
            .join(UserRolesModel, UserRolesModel.user_id == UserModel.id)
            .where(UserModel.email == email)
        )

        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise  InvalidCredentialsError()
        return UserRoleSchema.model_validate(result)