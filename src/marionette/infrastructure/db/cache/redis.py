from redis.asyncio import Redis

class RedisManager:
    def __init__(self, url: str) -> None:
        self._redis = Redis.from_url(url) # pyright: ignore[reportUnknownMemberType]

    async def dispose(self) -> None:
        await self._redis.aclose()

    @property
    def client(self) -> Redis:
        return self._redis
