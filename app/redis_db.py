from aioredis import Redis, from_url

from typing import Optional


class RedisManager:
    def __init__(self):
        self.redis_manager: Optional[Redis] = None

    async def init_redis(self):
        self.redis_manager = from_url(
            'redis://localhost', encoding='utf-8', decode_responses=True
        )

    async def close(self):
        await self.redis_manager.close()


redis_manager = RedisManager()
