import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.presentation.discord.plugins.profile.profile_group import profile_group

'''plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@profile_group.child
@crescent.command(guild=config.discord.main_guild_id)
class ProfileEditorCommand:
    async def callback(self, ctx: crescent.Context) -> None: ...
'''