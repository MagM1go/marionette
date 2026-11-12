import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.presentation.discord.plugins.roleplay.posting.posting_group import posting

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@posting.child
@crescent.command(
    name="perfomance",
    description="Объявить миру о... чём-либо.",
    guild=config.discord.guild.main,
)
class PerfomanceCommand:
    async def callback(self, ctx: crescent.Context) -> None: ...
