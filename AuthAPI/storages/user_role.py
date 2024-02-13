from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import create_async_session
from models.models import UserRole
from storages import AlchemyBaseStorage


class UserRoleStorage(AlchemyBaseStorage):
    table = UserRole
