from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    async def upload(self, file) -> dict:
        pass

    @abstractmethod
    async def download(self, name):
        pass
