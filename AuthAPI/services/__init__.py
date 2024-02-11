from abc import ABC, abstractmethod


class BaseService(ABC):
    pass


class AbstractCrudService(ABC):
    """
        CRUD для управления ролями:

            - создание роли,
            - удаление роли,
            - изменение роли,
            - просмотр всех ролей.
            - назначить пользователю роль
            - отобрать у пользователя роль
            - метод для проверки наличия прав у пользователя
    """
    @abstractmethod
    async def create_role(self, id: str, data):
        ''' создание роли '''
        pass

    @abstractmethod
    async def delete_role(self, id: str):
        ''' удаление роли '''
        pass

    @abstractmethod
    async def set_role(self, id, data):
        ''' изменение роли '''
        pass

    @abstractmethod
    async def show_all_role(self):
        ''' просмотр всех ролей '''
        pass

    @abstractmethod
    async def add_role(self, id: str, data, user):
        ''' назначить пользователю роль '''
        pass

    @abstractmethod
    async def deprive_role(self, id: str, user):
        ''' отобрать у пользователя роль '''
        pass

    @abstractmethod
    async def check_role(self, id: str, user):
        ''' проверка наличия прав у пользователя '''
        pass
