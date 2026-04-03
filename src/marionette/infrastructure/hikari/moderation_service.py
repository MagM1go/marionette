import hikari

from marionette.application.protocols.roleplay_moderation_protocol import RoleplayModeration


class HikariRoleplayModeration(RoleplayModeration):
    def __init__(self, cache: hikari.api.Cache) -> None:
        self._cache = cache

    def is_rp_location(self, location: object) -> bool:
        channel = location
        if not isinstance(channel, (hikari.GuildTextChannel, hikari.GuildThreadChannel)):
            return False

        if not channel or not channel.parent_id:
            return False

        parent = self._cache.get_guild_channel(channel.parent_id)
        if parent and parent.parent_id:
            parent = self._cache.get_guild_channel(parent.parent_id)

        return False
