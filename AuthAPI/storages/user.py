from models.models import User
from storages import AlchemyBaseStorage


class UserStorage(AlchemyBaseStorage):
    table = User
