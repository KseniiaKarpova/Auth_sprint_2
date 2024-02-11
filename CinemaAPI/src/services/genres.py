from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from services.base_service import BaseService
from storages.base_storage import BaseCache
from storages.cache_storage import RedisCache
from storages.genre_storage import GenreBaseStorage, GenreElasticStorage


class GenreService(BaseService):
    def __init__(self, cache: BaseCache, storage: GenreBaseStorage):
        self.cache = cache
        self.storage = storage

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_list(self, url: str) -> list[dict]:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_list()
            if data:
                await self.cache.put_to_cache(url, data)
        return data


@lru_cache()
def get_genre_service(
        cache: BaseCache = Depends(RedisCache),
        genre_storage: GenreBaseStorage = Depends(GenreElasticStorage),
) -> GenreService:
    return GenreService(cache, genre_storage)
