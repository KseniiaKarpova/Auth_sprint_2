from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Header, Body
from redis.asyncio import Redis

from db.redis import get_redis
from schemas.auth import (
    AuthSettingsSchema, LoginResponseSchema,
    UserCredentials, UserUpdate,
    UserLogin, UserData)
from services.auth import get_auth_service, AuthService
from core.handlers import get_jwt_handler, JwtHandler


router = APIRouter()


@AuthJWT.load_config
def get_auth_config():
    return AuthSettingsSchema()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    redis = get_redis()
    entry = await redis.get(jti)
    return entry and entry == "true"


@router.post("/login", response_model=LoginResponseSchema)
async def login(
        jwt_handler: JwtHandler = Depends(get_jwt_handler),
        credentials: UserLogin = Body()):
    return await jwt_handler.user_tokens(credentials=credentials)


@router.post(
    "/refresh",
    response_model=LoginResponseSchema,
    response_model_exclude_none=True)
async def refresh(
        jwt_handler: JwtHandler = Depends(get_jwt_handler),):
    return await jwt_handler.refresh_access_token()


@router.post("/logout")
async def logout(
        redis: Redis = Depends(get_redis),
        refresh_token: str = Header(..., alias="X-Access-Token"),
        access_token: str = Header(..., alias="X-Refresh-Token")):
    if access_token:
        await redis.setex(access_token, AuthSettingsSchema().access_expires, "true")
    if refresh_token:
        await redis.setex(refresh_token, AuthSettingsSchema().refresh_expires, "true")
    return {"detail": "User successfully logged out"}


@router.post(
        "/registration",
        response_model=UserData)
async def registration(
        user_credentials: UserCredentials,
        service: AuthService = Depends(get_auth_service)):
    return await service.registrate(data=user_credentials)


@router.patch("/user")
async def update_user(
        user_data: UserUpdate = Body(),
        jwt_handler: JwtHandler = Depends(get_jwt_handler),
        service: AuthService = Depends(get_auth_service)):
    current_user = await jwt_handler.get_current_user()
    return await service.update_user(data=user_data, user_id=current_user.uuid)
