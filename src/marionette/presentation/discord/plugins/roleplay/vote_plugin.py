import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer

from marionette.bootstrap.di.inject import inject

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    guild=config.discord.main_guild_id,
    name="vote",
    description="Отдать свой голос кому-либо (раз в 6 часов)",
)
class VoteCommand:
    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context) -> None: ...
