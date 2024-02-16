from functools import lru_cache
from uuid import UUID
from fastapi import Depends

from core.hasher import DataHasher
from services import BaseService
from storages.user import UserStorage
from schemas.auth import UserCredentials, UserUpdate
from exceptions import user_created, user_updated
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session


class AuthService(BaseService):
    def __init__(self, storage: UserStorage):
        self.storage = storage

    async def registrate(self, data: UserCredentials):
        hashed_password = await DataHasher().generate_word_hash(secret_word=data.password)
        await self.storage.create(params={
            'password': hashed_password,
            'login': data.login,
            'email': data.email,
        })
        return user_created

    async def is_super_user(self, login):
        status = await self.storage.exists(conditions={
            'login': login,
            'is_superuser': True
        })
        return status

    async def update_user(self, user_id: UUID, data: UserUpdate):
        await self.storage.update(
            conditions={
                "uuid": user_id,
            },
            values=data.dict(exclude_unset=True)
        )
        return user_updated


@lru_cache()
def get_auth_service(
    session: AsyncSession = Depends(create_async_session)
) -> AuthService:
    return AuthService(storage=UserStorage(session=session))
