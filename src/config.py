import os
from pathlib import Path
from pydantic import ConfigDict
from dynaconf import Dynaconf
from loguru import logger

from src.application.schemas.common import BaseSchema


class ApiConfig(BaseSchema):
    host: str = 'localhost'
    port: int = 8000
    project_name: str = 'base'

class DatabaseConfig(BaseSchema):
    host: str
    port: int
    username: str
    password: str
    database: str
    driver: str = 'postgresql+psycopg_async'

    @property
    def dsn(self, db = True) -> str:
        return f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'


class AuthConfig(BaseSchema):
    private_key_path: Path = 'src/application/servers/auth/keys/private.pem'
    public_key_path: Path = 'src/application/servers/auth/keys/public.pem'
    time: int = 1200
    algorithm: str = "RS256"

class DataConfig(BaseSchema):
    user_role_id: str

class RedisConfig(BaseSchema):
    host: str = 'redis'
    port: int = 6379
    password: str = 'redis'
    user: str = 'redis'
    user_password = 'redis'

class Config(BaseSchema):
    model_config = ConfigDict(extra='allow', from_attributes=True)
    api: ApiConfig
    database: DatabaseConfig
    auth: AuthConfig
    data: DataConfig
    redis: RedisConfig


def get_config() -> Config:
    dynaconf = Dynaconf(
        settings_files=[
            '././deploy/configs/config.toml'
        ],
        envvar_prefix='Liza',
        load_dotenv=True,
    )
    logger.info(dynaconf.api)
    return Config.model_validate(dynaconf)