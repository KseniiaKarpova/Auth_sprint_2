from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from services.base_service import BaseService
from storages.base_storage import BaseCache
from storages.cache_storage import RedisCache
from storages.person_storage import PersonBaseStorage, PersonElasticStorage


class PersonService(BaseService):
    def __init__(self, cache: BaseCache, storage: PersonBaseStorage):
        self.cache = cache
        self.storage = storage

    async def search_data(self, url: str, query, page_number: int, page_size: int):
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.search_data(query, page_number=page_number, page_size=page_size)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_person_films(self, url: str, id: UUID) -> list[dict]:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_person_films(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data


@lru_cache()
def get_person_service(
        cache: BaseCache = Depends(RedisCache),
        person_storage: PersonBaseStorage = Depends(PersonElasticStorage),
) -> PersonService:
    return PersonService(cache, person_storage)
