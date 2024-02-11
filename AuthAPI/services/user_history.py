from functools import lru_cache
from uuid import UUID

from core.params import QueryParams
from db.postgres import create_async_session
from fastapi import Depends
from models.models import UserHistory
from schemas.user_history import UserHistoryCreate
from services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from storages.user_history import UserHistoryStorage


class UserHistoryService(BaseService):
    def __init__(self, storage: UserHistoryStorage):
        self.storage = storage

    async def user_login_history(self, user_id: UUID) -> list[UserHistory]:
        return await self.storage.get_many(
            conditions={
                'user_id': user_id,
            },
        )

    async def save_login(self, data: UserHistoryCreate):
        pass


@lru_cache()
def get_user_history_service(
    session: AsyncSession = Depends(create_async_session),
    commons: QueryParams = Depends(QueryParams),
) -> UserHistoryService:
    return UserHistoryService(
        storage=UserHistoryStorage(
            session=session,
            limit=commons.page_size,
            offset=commons.page_number,
            order_by=commons.order_by))
