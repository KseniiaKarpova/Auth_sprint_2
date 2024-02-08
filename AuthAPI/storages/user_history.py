from models.models import UserHistory
from storages import AlchemyBaseStorage


class UserHistoryStorage(AlchemyBaseStorage):
    table = UserHistory
