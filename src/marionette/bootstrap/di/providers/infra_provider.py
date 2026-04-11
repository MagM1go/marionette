from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide

from marionette.application.protocols import PlayerAccessManager
from marionette.application.protocols.roleplay_moderation_protocol import RoleplayModeration
from marionette.bootstrap.config import config
from marionette.infrastructure.cache.redis import RedisManager
from marionette.infrastructure.services.discord.access_manager_service import DicsordAccessManager
from marionette.infrastructure.services.discord.moderation_service import HikariRoleplayModeration


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def redis_manager(self) -> AsyncGenerator[RedisManager]:
        manager = RedisManager(config.database.redis_url)
        yield manager
        await manager.dispose()

    discord_service = provide(DicsordAccessManager, provides=PlayerAccessManager)
    moderation_service = provide(HikariRoleplayModeration, provides=RoleplayModeration)
