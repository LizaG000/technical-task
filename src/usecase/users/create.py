from sqlalchemy.ext.asyncio import AsyncSession
from src.config import DataConfig
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate, CreateGate
from src.application.schemas.users import CreateUserSchema, UserSchema
from src.application.schemas.password import CreatePasswordSchema
from src.application.schemas.user_role import CreateUserRoleSchema
from src.usecase.users.schemas import RequestRegistrationSchema, ResponseRegistrationSchema
from src.infra.postgres.tables import UserModel, PasswordsModel, UserRolesModel
from dataclasses import dataclass
from src.application.servers.auth.hash_password import hash_password
from src.application.servers.auth.encoded_jwt import EncodedJwt

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[RequestRegistrationSchema, ResponseRegistrationSchema]):
    session: AsyncSession
    config: DataConfig
    encoded_jwt: EncodedJwt
    create_user: CreateReturningGate[UserModel, CreateUserSchema, UserSchema]
    create_password: CreateGate[PasswordsModel, CreatePasswordSchema]
    create_user_role: CreateGate[UserRolesModel, CreateUserRoleSchema]
    
    async def __call__(self, data: RequestRegistrationSchema) -> ResponseRegistrationSchema:
        async with self.session.begin():
            user = await self.create_user(CreateUserSchema(\
                first_name=data.first_name,
                middle_name=data.middle_name,
                last_name=data.last_name,
                email=data.email))
            password = await hash_password(data.password)
            await self.create_password(CreatePasswordSchema(
                user_id=user.id,
                password=password
            ))
            await self.create_user_role(CreateUserRoleSchema(
                user_id=user.id,
                role=self.config.user_role_id
            ))
            token = await self.encoded_jwt(user.id, 'user')
            return ResponseRegistrationSchema(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                token=token
            )



            
            
