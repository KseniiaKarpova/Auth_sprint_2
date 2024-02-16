from models.models import Role, User, UserRole
from sqlalchemy import func, select
from storages import AlchemyBaseStorage
from schemas.auth import SocialData
from core.hasher import DataHasher
from storages.social_account import SocialAccountStorage
from db.postgres import commit_async_session


class UserStorage(AlchemyBaseStorage):
    table = User

    async def with_roles(self, conditions: dict) -> User:
        user, roles = None, None
        _where = await self.generate_where(conditions=conditions)
        new_query = select(
            User,
            func.array_agg(Role.name).label('roles'),
            ).join(
                UserRole, User.uuid == UserRole.user_id, isouter=True).join(
                    Role, Role.uuid == UserRole.role_id, isouter=True).where(
                        _where).group_by(User.uuid)
        result = (await self.execute(query=new_query)).mappings().first()
        if result:
            user, roles = result.get('User'), result.get('roles', [])
        return user, roles

    async def create_with_social_acc(self, social_data: SocialData):
        self.commit_mode = False
        social_acc_storage = SocialAccountStorage(
                session=self.session,
                commit_mode=False)
        async with self.session:
            user: User = await self.create(params={
                'email': social_data.user.email,
                'login': social_data.user.email,
                'password': await DataHasher().random_password()
            })

            self.session.add(user)
            social_account = await social_acc_storage.create(
                {
                    'type': social_data.type,
                    'social_user_id': social_data.social_user_id,
                    'data': social_data.data,
                    'user_id': user.uuid
                    },
                    )
            self.session.add(social_account)
            await self.session.flush()
            await commit_async_session(self.session)
        return user, social_account
