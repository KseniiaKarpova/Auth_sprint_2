from models.models import SocialAccount
from storages import AlchemyBaseStorage


class SocialAccountStorage(AlchemyBaseStorage):
    table = SocialAccount
