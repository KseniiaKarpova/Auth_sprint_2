from db.postgres import create_async_session
from fastapi import Depends
from models.models import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from storages import AlchemyBaseStorage


class UserRoleStorage(AlchemyBaseStorage):
    table = UserRole
