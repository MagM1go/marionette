from typing import Any

import crescent
import hikari
import orjson
from hikari.internal import routes
from hikari.internal.data_binding import JSONObjectBuilder

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
        json_load: dict[str, Any] = orjson.loads(self.json_text)
        json = JSONObjectBuilder()

        for key, value in json_load.keys():
            json.put(key, value)

        await plugin.app._rest._request(compiled_route=routes.POST_CHANNEL_MESSAGES.compile(channel=self.channel), json=json)
        await ctx.respond("👍", flags=hikari.MessageFlag.EPHEMERAL)
