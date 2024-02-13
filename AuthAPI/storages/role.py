from models.models import Role
from storages import AlchemyBaseStorage


class RoleStorage(AlchemyBaseStorage):
    table = Role
