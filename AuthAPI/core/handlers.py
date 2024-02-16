import http
import json
import time
from typing import Optional

from async_fastapi_jwt_auth import AuthJWT
from core.config import settings
from core.hasher import DataHasher
from db.postgres import create_async_session
from db.redis import get_redis
from exceptions import (forbidden_error, incorrect_credentials, server_error,
                        unauthorized)
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from models.models import User
from schemas.auth import (AuthSettingsSchema, JWTUserData, LoginResponseSchema,
                          UserLogin)
from sqlalchemy.ext.asyncio import AsyncSession
from storages.user import UserStorage
from storages.user_history import UserHistoryStorage


@AuthJWT.load_config
def get_auth_config():
    return AuthSettingsSchema()


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.jwt_algorithm])
        if decoded_token['exp'] < time.time():
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid or expired token.')
        return decoded_token
    except Exception:
        raise server_error


async def jwt_user_data(subject: dict):
    subject: dict = json.loads(subject)
    login, uuid = subject.get('login'), subject.get('uuid')
    if not login or not uuid:
        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
    return JWTUserData(login=login, uuid=uuid)


class JWTBearer(HTTPBearer):
    def __init__(
            self, auto_error: bool = True,
            token_type: str = 'access'):
        self.token_type = token_type
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        await self.check_credentials(credentials=credentials)
        decoded_token = decode_token(credentials.credentials)
        subject, jti, type = await self.check_fields(decoded_token=decoded_token)
        if type != self.token_type:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='wrong token')
        return {
            'subject': subject,
            'jti': jti,
            'type': type
        }

    async def check_denylist(self, jti):
        redis = get_redis()
        denied = await redis.get(jti)
        if denied:
            raise forbidden_error

    async def check_credentials(self, credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Only Bearer token might be accepted')

    async def check_fields(self, decoded_token: dict):
        subject: dict = decoded_token.get('sub')
        jti = decoded_token.get('jti')
        type = decoded_token.get('type')
        if not subject or not jti or not type:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid or expired token.')
        await self.check_denylist(jti=jti)
        return subject, jti, type


class JwtHandler:
    def __init__(self, session: AsyncSession,
                 jwt_data: dict = None) -> None:

        self.jwt_data = jwt_data
        self.storage = UserStorage(session=session)

    async def is_super_user(self):
        user = await self.get_current_user()
        exists = await self.storage.exists(conditions={
            'uuid': user.uuid,
            'is_superuser': True
        })
        if exists is False:
            raise forbidden_error
        return await jwt_user_data(subject=self.jwt_data.get('subject'))

    async def get_current_user(self) -> User:
        return await jwt_user_data(subject=self.subject)

    @property
    def subject(self):
        return self.jwt_data.get('subject')


class AuthHandler:
    def __init__(
            self,
            Authorize: AuthJWT,
            session: AsyncSession) -> None:
        self.auth = Authorize
        self.observer = UserHistoryStorage(session=session)
        self.storage = UserStorage(session=session)

    async def generate_access_token(self, subject):
        return await self.auth.create_access_token(subject=subject, fresh=True)

    async def generate_refresh_token(self, subject):
        return await self.auth.create_refresh_token(subject=subject)

    async def refresh_access_token(self, subject: dict) -> LoginResponseSchema:
        return LoginResponseSchema(
            access_token=await self.generate_access_token(subject=subject))

    async def check_credentials(self, credentials: UserLogin) -> User:
        user, roles = await self.storage.with_roles(conditions={
            'login': credentials.login,
        })
        if not user:
            raise incorrect_credentials
        is_valid = await DataHasher().verify(secret_word=credentials.password, hashed_word=user.password)
        if is_valid is False:
            raise unauthorized
        return user, roles

    async def user_tokens(self, credentials: UserLogin) -> LoginResponseSchema:
        user, roles = await self.check_credentials(credentials)
        subject = json.dumps({
            'login': user.login,
            'uuid': str(user.uuid),
            'roles': roles
        })

        access_token = await self.generate_access_token(subject=subject)
        refresh_token = await self.generate_refresh_token(subject=subject)

        if self.observer:
            await self.observer.create(
                params={
                    "user_id": user.uuid,
                    "user_agent": credentials.agent,
                    "refresh_token": refresh_token,
                }
            )
        return LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )


def get_auth_handler(
    auth: AuthJWT = Depends(),
    session: AsyncSession = Depends(create_async_session),
) -> AuthHandler:
    return AuthHandler(session=session, Authorize=auth)


def require_access_token(
    jwt_data: dict = Depends(JWTBearer(token_type='access')),
    session: AsyncSession = Depends(create_async_session),
) -> JwtHandler:
    return JwtHandler(jwt_data=jwt_data, session=session)


def require_refresh_token(
    jwt_data: dict = Depends(JWTBearer(token_type='refresh')),
    session: AsyncSession = Depends(create_async_session),
) -> JwtHandler:
    return JwtHandler(jwt_data=jwt_data, session=session)
