from abc import ABC
from typing import Any


class BaseService(ABC):
    async def get_data_by_id(self, *args, **kwargs) -> Any:
        pass

    async def get_data_list(self, *args, **kwargs) -> Any:
        pass

    async def search_data(self, *args, **kwargs) -> Any:
        pass
