import typing as t

from redis.asyncio import Redis

from marionette.application.protocols import ICooldownRepository


class CooldownRepository(ICooldownRepository):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @t.override
    async def is_on_cooldown(self, key: str) -> bool:
        return await self.redis.get(key) is not None

    @t.override
    async def set_cooldown(self, key: str, seconds: int) -> None:
        await self.redis.set(key, 1, ex=seconds)
