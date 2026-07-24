from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka import provide_all
from fastapi import Request

from src.config import Config, DataConfig
from src.config import ApiConfig
from src.config import DatabaseConfig
from src.config import AuthConfig
from src.config import RedisConfig

from src.usecase.auth.registration import RegistrationUserUsecase
from src.usecase.auth.login import LoginUserUsecase
from src.usecase.auth.logout import LogoutUserUsecase
from src.usecase.users.update import UpdateUserUsecase
from src.usecase.users.delete import DeleteUserUsecase
from src.usecase.user_roles.create import CreateUserRoleUsecase
from src.usecase.user_roles.delete import DeleteUserRoleUsecase
from src.usecase.users.get import GetUserRoleUsecase
from src.usecase.permission.update import UpdatePermissionUsecase
from src.usecase.permission.get_all import GetAllPermissionUsecase
from src.usecase.products.get_all import GetAllProductsUsecase
from src.usecase.products.create import CreateProductUsecase

class MainProvider(Provider):
    scope = Scope.REQUEST

    _provide_config = from_context(provides=Config, scope=Scope.APP) 

    @provide(scope=Scope.APP)
    async def _get_api_config(self, config: Config) -> ApiConfig:
        return config.api
    
    @provide(scope=Scope.APP)
    async def _get_database_config(self, config: Config) -> DatabaseConfig:
        return config.database

    @provide(scope=Scope.APP)
    async def _get_auth_config(self, config: Config) -> AuthConfig:
        return config.auth
    
    @provide(scope=Scope.APP)
    async def _get_data_config(self, config: Config) -> DataConfig:
        return config.data
    
    @provide(scope=Scope.APP)
    async def _get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis
    
    _request = from_context(provides=Request, scope=Scope.REQUEST)

    _get_usecases = provide_all(
        RegistrationUserUsecase,
        LoginUserUsecase,
        LogoutUserUsecase,
        UpdateUserUsecase,
        DeleteUserUsecase,
        CreateUserRoleUsecase,
        GetUserRoleUsecase,
        DeleteUserRoleUsecase,
        UpdatePermissionUsecase,
        GetAllPermissionUsecase,
        GetAllProductsUsecase,
        CreateProductUsecase,
    )

