from logging import config as logging_config

from core.logger import LOGGING
from fastapi import Query
from pydantic import Field
from pydantic_settings import BaseSettings

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


class Settings(BaseSettings):
    project_name: str = Field('Async API', env='CINEMA_API_PROJECT_NAME')
    redis_port: int = Field(6379, env='REDIS_PORT')
    es_host: str = Field('elasticsearch', env='ES_HOST')
    es_port: int = Field(9200, env='ES_PORT')
    redis_host: str = Field('redis', env='REDIS_HOST')
    jaeger_host: str = Field('auth_jaeger', env='JAEGER_HOST')
    jaeger_port: int = Field(6831, env='JAEGER_PORT')


class FileAPISettings(BaseSettings):
    file_api_host: str = Field('file_api', env='FILE_API_HOST')
    file_api_port: int = Field(7070, env='FILE_API_PORT')
    file_api_url: str = Field('/api/v1/', env='FILE_API_URL')


file_api_settings = FileAPISettings()
