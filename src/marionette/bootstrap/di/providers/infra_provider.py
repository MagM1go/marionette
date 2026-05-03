from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide

from marionette.bootstrap.config import config
from marionette.infrastructure.cache.redis import RedisManager


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def redis_manager(self) -> AsyncGenerator[RedisManager]:
        manager = RedisManager(config.database.redis_url)
        yield manager
        await manager.dispose()
