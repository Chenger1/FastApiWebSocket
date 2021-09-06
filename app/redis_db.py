from aioredis import Redis, from_url

from typing import Optional


class RedisManager:
    def __init__(self):
        self.redis_manager: Optional[Redis] = None

    async def init_redis(self):
        self.redis_manager = from_url(
            'redis://localhost', encoding='utf-8', decode_responses=True
        )

    async def set(self, key, value):
        return await self.redis_manager.set(key, value)

    async def get(self, key):
        return await self.redis_manager.get(key)

    async def manual_get(self, method, key):
        return await getattr(self.redis_manager, method)(key)

    async def manual_set(self, method, key, value):
        return await getattr(self.redis_manager, method)(key, value)

    async def close(self):
        await self.redis_manager.close()


redis_manager = RedisManager()
