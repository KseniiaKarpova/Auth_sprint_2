from redis.asyncio import Redis

from core import config

settings = config.APPSettings()
redis: Redis | None = Redis(host=settings.redis.host, port=settings.redis.port)


def get_redis() -> Redis | None:
    return redis
