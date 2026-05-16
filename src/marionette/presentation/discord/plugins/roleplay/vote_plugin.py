import crescent
import hikari

from marionette.application.usecases.vote_usecase import VoteUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.ui.voting.vote_view import VoteView

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    guild=config.discord.main_guild_id,
    name="vote",
    description="Отдать свой голос кому-либо (раз в 24 часа)",
)
class VoteCommand:
    user = crescent.option(hikari.User, "Пользователь")
    character_name = crescent.option(str, "Персонаж")

    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context, usecase: Inject[VoteUseCase]) -> None:
        view = VoteView(usecase, self.user, self.character_name)
        await ctx.respond(components=view)
        plugin.model.component_client.start_view(view)
