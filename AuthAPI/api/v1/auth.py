from core.handlers import (AuthHandler, JwtHandler, get_auth_handler,
                           require_access_token, require_refresh_token)
from db.redis import get_redis
from fastapi import APIRouter, Body, Depends, Header
from redis.asyncio import Redis
from schemas.auth import (AuthSettingsSchema, LoginResponseSchema,
                          UserCredentials, UserLogin, UserUpdate)
from services.auth import AuthService, get_auth_service

router = APIRouter()


@router.post("/login", response_model=LoginResponseSchema)
async def login(
        auth: AuthHandler = Depends(get_auth_handler),
        credentials: UserLogin = Body()):
    return await auth.user_tokens(credentials=credentials)


@router.post(
    "/refresh",
    response_model=LoginResponseSchema,
    response_model_exclude_none=True)
async def refresh(
        jwt_handler: JwtHandler = Depends(require_refresh_token),
        auth: AuthHandler = Depends(get_auth_handler),
        ):
    return await auth.generate_refresh_token(subject=jwt_handler.subject)


@router.post("/logout")
async def logout(
        redis: Redis = Depends(get_redis),
        jwt_handler: JwtHandler = Depends(require_refresh_token),
        refresh_token: str = Header(..., alias="X-Access-Token"),
        access_token: str = Header(..., alias="X-Refresh-Token")):
    if access_token:
        await redis.setex(access_token, AuthSettingsSchema().access_expires, "true")
    if refresh_token:
        await redis.setex(refresh_token, AuthSettingsSchema().refresh_expires, "true")
    return {"detail": "User successfully logged out"}


@router.post("/registration")
async def registration(
        user_credentials: UserCredentials,
        service: AuthService = Depends(get_auth_service)):
    return await service.registrate(data=user_credentials)


@router.patch("/user")
async def update_user(
        user_data: UserUpdate = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: AuthService = Depends(get_auth_service),
        ):
    current_user = await jwt_handler.get_current_user()
    return await service.update_user(data=user_data, user_id=current_user.uuid)
