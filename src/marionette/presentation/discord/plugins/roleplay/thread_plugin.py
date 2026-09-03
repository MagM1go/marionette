import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.presentation.discord.presenters.thread_presenter import ThreadPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    name="thread", description="Создать РП ветку", guild=config.discord.main_guild_id, default_member_permissions=hikari.Permissions.ADMINISTRATOR
)
class RoleplayThreadCreateCommand:
    name = crescent.option(str, "название ветки")
    description = crescent.option(str, "описание ветки")
    paparazzi = crescent.option(bool, "папарацци")

    async def callback(self, ctx: crescent.Context) -> None:
        message = await ctx.app.rest.create_message(
            ctx.channel_id, component=ThreadPresenter.present(self.name, self.description), flags=hikari.MessageFlag.IS_COMPONENTS_V2
        )
        await ctx.app.rest.create_message_thread(
            ctx.channel_id, message, self.name if not self.paparazzi else config.discord.paparazzi_trigger_channel_prefix + " | " + self.name
        )
        await ctx.respond(ThreadPresenter.success(), ephemeral=True)
