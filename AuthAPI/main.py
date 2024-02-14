import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import auth, role, user_history
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from core import config
from utils.jaeger import configure_tracer
from core.logger import LOGGING
from db import postgres, redis
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from utils.constraint import RequestLimit

settings = config.APPSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_tracer(host=settings.jaeger.host, port=settings.jaeger.port, service_name=settings.project_name)

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


FastAPIInstrumentor.instrument_app(app)


@app.middleware('http')
async def before_request(request: Request, call_next):
    user = request.headers.get('X-Forwarded-For')
    result = await RequestLimit().is_over_limit(user=user)
    if result:
        return ORJSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={'detail': 'Too many requests'}
        )

    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response


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
        reload=True,
    )
