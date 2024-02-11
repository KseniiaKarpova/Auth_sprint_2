from typing import Optional

from redis.asyncio import Redis

redis: Optional[Redis] = None


def get_redis() -> Optional[Redis]:
    return redis
