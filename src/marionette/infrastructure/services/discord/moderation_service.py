from contextlib import suppress

import hikari

from marionette.application.protocols.roleplay_moderation_protocol import RoleplayModeration
from marionette.application.protocols.types import LocationId
from marionette.bootstrap.config import config


class HikariRoleplayModeration(RoleplayModeration):
    def __init__(self, cache: hikari.api.Cache, rest: hikari.api.RESTClient) -> None:
        self._cache = cache
        self._rest = rest

    async def is_rp_location(self, location_id: LocationId) -> bool:
        channel = await self._get_guild_channel(location_id)
        if not isinstance(channel, (hikari.GuildTextChannel, hikari.GuildThreadChannel)):
            return False

        if not channel or not channel.parent_id:
            return False

        parent = await self._get_guild_channel(channel.parent_id)
        if parent and parent.parent_id:
            parent = await self._get_guild_channel(parent.parent_id)

        if parent is None:
            return False

        return parent.id in config.discord.rp_categories

    async def _get_guild_channel(
        self,
        channel_id: hikari.Snowflakeish,
    ) -> hikari.GuildChannel | None:
        channel = self._cache.get_guild_channel(channel_id) or self._cache.get_thread(channel_id)
        if channel is not None:
            return channel

        with suppress(hikari.NotFoundError):
            fetched_channel = await self._rest.fetch_channel(channel_id)
            if isinstance(fetched_channel, hikari.GuildChannel):
                return fetched_channel

        return None
