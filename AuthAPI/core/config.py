from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

logging_config.dictConfig(LOGGING)


class PostgresDbSettings(BaseSettings):
    host: str = ...
    user: str = ...
    port: int = ...
    db: str = ...
    password: str = ...

    model_config = SettingsConfigDict(env_prefix='auth_postgres_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class HasherSettings(BaseSettings):
    algorithm: str = ...
    rounds: int = ...
    model_config: str = SettingsConfigDict(env_prefix='hasher_')


class JaegerSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='jaeger_')


class APPSettings(BaseSettings):
    project_name: str = 'Auth API'
    db: PostgresDbSettings = PostgresDbSettings()
    db_dsn: str = f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}'
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()
    jaeger: JaegerSettings = JaegerSettings()


settings = APPSettings()
