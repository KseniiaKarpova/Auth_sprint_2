from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    async def get(self, bucket: str, short_name: str):
        pass

    @abstractmethod
    async def save(self, file, bucket: str, path: str):
        pass
