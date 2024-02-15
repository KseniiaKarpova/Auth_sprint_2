from datetime import datetime

from db.redis import get_redis


class RequestLimit:
    DURATION = 60  # 1min
    LIMIT = 200

    def __init__(self, duration: int = None, limit: int = None):
        self.pipeline = get_redis().pipeline(transaction=True)
        self.duration = duration or RequestLimit.DURATION
        self.limit = limit or RequestLimit.LIMIT

    async def is_over_limit(self, user: str) -> bool:
        key = f'{user}:{datetime.now().minute}'
        await self.pipeline.incr(key)
        await self.pipeline.expire(key, self.duration)
        result = await self.pipeline.execute()
        if result[0] > self.limit:
            return True
        return False
