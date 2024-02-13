import json
from typing import Any

from db.redis import get_redis
from redis.asyncio import Redis
from storages.base_storage import BaseCache


class RedisCache(BaseCache):
    CACHE_EXPIRE_IN_SECONDS = 300

    def __init__(self, expire: int = None):
        self.redis: Redis = get_redis()
        self.expire = expire or RedisCache.CACHE_EXPIRE_IN_SECONDS

    async def get_from_cache(self, url: str):
        result = await self.redis.get(
            str(url),
        )
        if result:
            result = json.loads(result)
        return result

    async def put_to_cache(self, url: str, data: Any):
        data = json.dumps(data)
        await self.redis.setex(name=str(url), value=data, time=self.expire)
