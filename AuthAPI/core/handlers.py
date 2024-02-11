import json
from functools import lru_cache
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from core.hasher import DataHasher
from db.postgres import create_async_session
from exceptions import forbidden_error, incorrect_credentials, unauthorized
from fastapi import Depends
from models.models import User
from schemas.auth import JWTUserData, LoginResponseSchema, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from storages.user import UserStorage
from storages.user_history import UserHistoryStorage


class JWTCoverter:
    async def get_data(self, payload: dict):
        return json.loads(payload)

    async def convert_data(self, payload: dict):
        return json.dumps(payload)


class JwtHandler:
    def __init__(self,
                 Authorize: AuthJWT,
                 jwt_converter: JWTCoverter,
                 storage: UserStorage,
                 observer: UserHistoryStorage,
                 ) -> None:
        self.auth = Authorize
        self.jwt_converter = jwt_converter
        self.storage = storage
        self.observer = observer

    async def generate_access_token(self, subject):
        return await self.auth.create_access_token(subject=subject, fresh=True)

    async def generate_refresh_token(self, subject):
        return await self.auth.create_refresh_token(subject=subject)

    async def get_current_user(self) -> JWTUserData:
        """
        Dependency to get the current user from the JWT token.
        """
        await self.auth.jwt_required()
        jwt_subject = await self.auth.get_jwt_subject()
        subject = await self.jwt_converter.get_data(payload=jwt_subject)
        return JWTUserData(
            login=subject['login'],
            uuid=UUID(subject['uuid']),
        )

    async def is_super_user(self, current_user: JWTUserData = Depends(get_current_user)):
        exists = await self.storage.exists(conditions={
            'uuid': current_user.uuid,
            'is_superuser': True
        })
        if exists is False:
            raise forbidden_error
        return current_user

    async def check_credentials(self, credentials: UserLogin) -> User:
        user = await self.storage.get(conditions={
                'login': credentials.login
            })
        if not user:
            raise incorrect_credentials
        is_valid = await DataHasher().verify(secret_word=credentials.password, hashed_word=user.password)
        if is_valid is False:
            raise unauthorized
        return user

    async def user_tokens(self, credentials: UserLogin) -> LoginResponseSchema:
        user = await self.check_credentials(credentials)
        subject = await self.jwt_converter.convert_data({
            'login': user.login,
            'uuid': str(user.uuid)
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

    async def refresh_access_token(self) -> LoginResponseSchema:
        await self.auth.jwt_refresh_token_required()
        jwt_subject = await self.auth.get_jwt_subject()
        return LoginResponseSchema(
            access_token=await self.generate_access_token(subject=jwt_subject))


@lru_cache()
def get_jwt_handler(
    Authorize=Depends(AuthJWT),
    session: AsyncSession = Depends(create_async_session),
    jwt_converter=Depends(JWTCoverter),
) -> JwtHandler:
    return JwtHandler(
        Authorize=Authorize,
        jwt_converter=jwt_converter,
        storage=UserStorage(session=session),
        observer=UserHistoryStorage(session=session))
