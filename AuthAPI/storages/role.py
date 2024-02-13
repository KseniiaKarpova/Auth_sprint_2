from models.models import Role
from sqlalchemy.ext.asyncio import AsyncSession
from storages import AlchemyBaseStorage


class RoleStorage(AlchemyBaseStorage):
    table = Role
