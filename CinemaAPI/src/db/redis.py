from redis.asyncio import Redis

from typing import Optional

redis: Optional[Redis] = None


def get_redis() -> Optional[Redis]:
    return redis
