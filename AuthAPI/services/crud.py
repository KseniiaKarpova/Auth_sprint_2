from db.postgres import create_async_session
from fastapi import Depends
from services import AbstractCrudService
from sqlalchemy.ext.asyncio import AsyncSession
from storages.role import RoleStorage
from storages.user_role import UserRoleStorage


class CrudService(AbstractCrudService):
    def __init__(
            self,
            storage_user_role: UserRoleStorage,
            storage_role: RoleStorage):
        self.storage_user_role = storage_user_role
        self.storage_role = storage_role

    async def create_role(self, name: str):
        ''' создание роли '''
        res = await self.storage_role.create(params={
            'name': name
        })
        return res

    async def delete_role(self, type: str, val):
        ''' удаление роли '''
        res = await self.storage_role.delete(conditions={
            type: val
        })
        return res['rowcount']

    async def set_role(self, old_data=dict, new_data=dict):
        ''' изменение роли '''
        res = await self.storage_role.update(old_data, new_data)
        return res['rowcount']

    async def show_all_role(self):
        ''' просмотр всех ролей '''
        res = await self.storage_role.get_many({})
        return res

    async def add_role(self, user_id: str, role_id: str):
        ''' назначить пользователю роль '''
        res = await self.storage_user_role.create(params={
            'user_id': user_id,
            'role_id': role_id
        })
        return res

    async def deprive_role(self, user_id: str, role_id: str):
        ''' отобрать у пользователя роль '''
        res = await self.storage_user_role.delete(conditions={
            'user_id': user_id,
            'role_id': role_id
        })
        return res['rowcount']

    async def check_role(self, user_id, role_id):
        ''' проверка наличия прав у пользователя '''
        res = await self.storage_user_role.exists(conditions={
            'user_id': user_id,
            'role_id': role_id
        })
        return res


def get_crud_service(
    session: AsyncSession = Depends(create_async_session)
) -> CrudService:
    return CrudService(
        storage_user_role=UserRoleStorage(session=session),
        storage_role=RoleStorage(session=session))
