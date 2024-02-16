from logging import config as logging_config

from core.logger import LOGGING
from fastapi import Query
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class QueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


class FileAPISettings(BaseSettings):
    host: str = Field('file_api', env='FILE_API_HOST')
    port: int = Field(7070, env='FILE_API_PORT')
    url: str = Field('/api/v1/', env='FILE_API_URL')
    model_config: str = SettingsConfigDict(env_prefix='file_api_')

    @property
    def full_path(self):
        return f"http://{self.host}:{self.port}{self.url}"


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class Settings(BaseSettings):
    project_name: str = Field('Async API', env='CINEMA_API_PROJECT_NAME')
    redis_port: int = Field(6379, env='REDIS_PORT')
    es_host: str = Field('elasticsearch', env='ES_HOST')
    es_port: int = Field(9200, env='ES_PORT')
    redis_host: str = Field('redis', env='REDIS_HOST')
    jaeger_host: str = Field('auth_jaeger', env='JAEGER_HOST')
    jaeger_port: int = Field(6831, env='JAEGER_PORT')
    jaeger_enable: bool = Field(False, env='JAEGER_ENABLE')
    auth: AuthSettings = AuthSettings()
    file_api: FileAPISettings = FileAPISettings()


settings = Settings()
