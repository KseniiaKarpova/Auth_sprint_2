import logging
from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from api.v1 import auth, role, user_history
from core import config
from core.logger import LOGGING
from db import postgres, redis

settings = config.APPSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    postgres.async_engine = create_async_engine(
            settings.db_dsn,
            poolclass=QueuePool,
            pool_pre_ping=True, pool_size=20, pool_timeout=30)
    postgres.async_session_factory = sessionmaker(
            postgres.async_engine,
            expire_on_commit=False,
            autoflush=True,
            class_=AsyncSession)
    yield
    await postgres.async_engine.dispose()
    postgres.async_session_factory.close_all()
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description="Auth logic",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(router=auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(router=role.router, prefix="/api/v1/role", tags=["role"])
app.include_router(router=user_history.router, prefix="/api/v1/user_history", tags=["role"])

if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
