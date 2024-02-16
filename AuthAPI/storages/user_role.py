from models.models import UserRole
from storages import AlchemyBaseStorage


class UserRoleStorage(AlchemyBaseStorage):
    table = UserRole
