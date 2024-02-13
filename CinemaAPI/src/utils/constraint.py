from db.redis import get_redis
from redis.asyncio import Redis


class RequestLimit:

    def __init__(self):
        self.pipeline: Redis = get_redis().pipeline()

    async def is_over_limit(self, user: str) -> bool:
        return False
