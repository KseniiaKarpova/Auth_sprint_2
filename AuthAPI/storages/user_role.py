from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import create_async_session
from models.models import UserRole
from storages import AlchemyBaseStorage


class UserRoleStorage(AlchemyBaseStorage):
    table = UserRole

    def __init__(self, session: AsyncSession = None) -> None:
        super().__init__(session)


def get_user_role_storage(session=Depends(create_async_session)):
    return UserRoleStorage(session=session)
