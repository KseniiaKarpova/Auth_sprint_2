from models.models import User, UserRole, Role
from storages import AlchemyBaseStorage
from sqlalchemy import select, func


class UserStorage(AlchemyBaseStorage):
    table = User

    async def with_roles(self, login: str) -> User:
        user, roles = None, None
        new_query = select(
            User,
            func.array_agg(Role.name).label('roles'),
            ).join(
                UserRole, User.uuid == UserRole.user_id, isouter=True).join(
                    Role, Role.uuid == UserRole.role_id, isouter=True).where(
                        User.login == login).group_by(User.uuid)
        result = (await self.execute(query=new_query)).mappings().first()
        if result:
            user, roles = result.get('User'), result.get('roles', [])
        return user, roles
