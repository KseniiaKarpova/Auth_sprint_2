from logging import config as logging_config
import os

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class BucketSettings(BaseSettings):
    bucket_movies: str = os.getenv('BUCKET_MOVIES', 'movies')
    movies_path: str = Field('movie/')


class Settings(BaseSettings):
    project_name: str = os.getenv('PROJECT_NAME', 'File API')

    minio_host: str = os.getenv('S3_HOST', 'minio')
    minio_port: int = os.getenv('S3_PORT', 9000)
    minio_user: str = os.getenv('S3_USER', 'adminS3')
    minio_password: str = os.getenv('S3_PASSWORD', 'adminS3pass')

    observer_host: str = os.getenv('FILE_POSTGRES_HOST')
    observer_port: int = os.getenv('FILE_POSTGRES_PORT')
    observer_user: str = os.getenv('FILE_POSTGRES_USER')
    observer_password: str = os.getenv('FILE_POSTGRES_PASSWORD')
    observer_database: str = os.getenv('FILE_POSTGRES_NAME')
    observer_type: str = os.getenv('OBS_TYPE')


bucket_settings = BucketSettings()
