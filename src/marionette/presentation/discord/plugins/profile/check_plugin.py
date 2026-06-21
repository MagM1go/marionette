import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import inject
from marionette.presentation.discord.plugins.profile.profile_group import profile_group

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@profile_group.child
@crescent.command(guild=config.discord.main_guild_id, name="check", description="Посмотреть профиль пользователя")
class ProfileCheckCommand:
    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.respond(f"hello {ctx.user.mention}")
