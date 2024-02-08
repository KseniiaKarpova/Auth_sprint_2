import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import create_async_engine

from api.v1 import file
from core import config
from core.logger import LOGGING
from db import minio, postgres
from models.file_db import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

settings = config.Settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    minio.minio = Minio(
        endpoint=f'{settings.minio_host}:{settings.minio_port}',
        access_key=settings.minio_user,
        secret_key=settings.minio_password,
        secure=False,
    )
    result = await minio.minio.bucket_exists(config.bucket_settings.bucket_movies)
    if not result:
        await minio.minio.make_bucket(config.bucket_settings.bucket_movies)

    postgres.engine = create_async_engine(
        f'{settings.observer_type}://{settings.observer_user}:{settings.observer_password}@{settings.observer_host}:{settings.observer_port}/{settings.observer_database}',
        echo=True,
    )
    postgres.async_session = async_sessionmaker(postgres.engine, class_=AsyncSession, expire_on_commit=False)

    yield
    await postgres.engine.dispose()


app = FastAPI(
    title=settings.project_name,
    description="Upload and download files",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(file.router, prefix='/api/v1', tags=['file'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
