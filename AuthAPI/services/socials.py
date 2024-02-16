from fastapi import Depends
from services import BaseService
from storages.user import UserStorage, User
from abc import abstractmethod
from schemas.auth import SocialData, UserLogin
from core.handlers import AuthHandler
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from async_fastapi_jwt_auth import AuthJWT


class AbstractSocialAuthService(BaseService):
    @abstractmethod
    async def authorize(self, ):
        ''' создание юзера по эмайл '''
        pass


class SocialAccountService(AbstractSocialAuthService):
    def __init__(
            self,
            user_storage: UserStorage,
            auth_handler: AuthHandler,
    ) -> None:
        self.user_storage = user_storage
        self.auth_handler = auth_handler

    async def authorize(self, social_data: SocialData):
        user: User = await self.user_storage.with_roles(conditions={
            'email': social_data.user.email,
        })
        if not user:
            user, social_account = await self.user_storage.create_with_social_acc(social_data=social_data)

        return await self.auth_handler.user_tokens(credentials=UserLogin(
            login=user.login,
            password=user.password,
        ))


def get_social_service(
    session: AsyncSession = Depends(create_async_session),
    auth: AuthJWT = Depends(),
) -> SocialAccountService:
    return SocialAccountService(
        user_storage=UserStorage(session=session),
        auth_handler=AuthHandler(
            session=session,
            Authorize=auth))
