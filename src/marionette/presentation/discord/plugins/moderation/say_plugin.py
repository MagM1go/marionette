import crescent
import hikari
from hikari.internal import routes

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    name="say",
    description="Сказать чего-то от имени бота",
    default_member_permissions=hikari.Permissions.ADMINISTRATOR,
    guild=config.discord.guild.main,
)
class SayCommand:
    channel = crescent.option(str, "ID канала, куда нужно слать")
    json_text = crescent.option(str, "Сырой JSON (hikari)")

    async def callback(self, ctx: crescent.Context) -> None:
        await plugin.app._rest._request(compiled_route=routes.POST_CHANNEL_MESSAGES.compile(channel=self.channel), json=self.json_text)
        await ctx.respond("👍", flags=hikari.MessageFlag.EPHEMERAL)
