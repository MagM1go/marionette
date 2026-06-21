import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.queries.characters import CharacterQueries
from marionette.application.usecases.vote_usecase import VoteUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.exceptions import HasNoCharacters
from marionette.presentation.discord.presenters.vote_presenter import VotePresenter
from marionette.presentation.discord.ui.voting.vote_modal import VoteModal
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

    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context, usecase: Inject[VoteUseCase], query: Inject[CharacterQueries]) -> None:
        character_names = [character.name for character in await query.get_user_characters(UserId(self.user.id))]
        if not character_names:
            raise HasNoCharacters()

        modal = VoteModal(usecase, ctx.user.id, UserId(self.user.id), character_names)
        view = VoteView(modal=modal)
        await ctx.respond(VotePresenter.present_vote_button(), components=view, ephemeral=True)
        plugin.model.component_client.start_view(view)
