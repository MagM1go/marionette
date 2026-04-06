import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    guild=config.discord.main_guild_id,
    name="initialize",
    description="Административная команда для инициализации онбординга",
    default_member_permissions=hikari.Permissions.ADMINISTRATOR,
)
class InitializeCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        ...
