import hikari

from marionette.application.protocols.roleplay_moderation_protocol import RoleplayModeration


class HikariRoleplayModeration(RoleplayModeration):
    # скорее всего тоже будет переделано и пересмотрено
    def is_rp_location(self, channel: hikari.PartialChannel, cache: hikari.api.Cache):
        if not isinstance(channel, (hikari.GuildTextChannel, hikari.GuildThreadChannel)):
            return False

        if not channel or not channel.parent_id:
            return False

        parent = cache.get_guild_channel(channel.parent_id)
        if parent and parent.parent_id:
            parent = cache.get_guild_channel(parent.parent_id)

        return False
