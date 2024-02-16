from services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from storages.user import UserStorage
from storages import AlchemyBaseStorage
from abc import abstractmethod


class AbstractSocialAuthService(BaseService):
    @abstractmethod
    async def authorize(self, ):
        ''' создание юзера по эмайл '''
        pass
    


class SocialAuthService(AbstractSocialAuthService):
    def __init__(self, storage: AlchemyBaseStorage, ) -> None:
        self.storage = storage
    
    async def authorize(self, id: str, data):
        pass
