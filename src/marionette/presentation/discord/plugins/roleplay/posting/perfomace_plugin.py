from datetime import datetime

import crescent
import hikari
from hikari.interactions import InteractionType

from marionette.application.protocols import CharacterId, UserId
from marionette.application.usecases.vote.perfomance_vote_usecase import PerfomanceVoteUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.plugins.roleplay.posting.posting_group import posting
from marionette.presentation.discord.presenters.perfomance_presenter import PerfomancePresenter
from marionette.presentation.discord.ui.posting.perfomance_keyboard import PerfomanceView

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()

ID_STARTS = {"like": 1, "ok": 0, "dislike": -1}


@plugin.include
@posting.child
@crescent.command(name="perfomance", description="Объявить миру о... чём-либо.", guild=config.discord.guild.main)
class PerfomanceCommand:
    """
    Я бы мог сделать это завязанным на БД бота, чтобы в случае чего перфомансы можно было восстановить,
    но это всего лишь редирект, так что не думаю, что это сильно надо
    """

    title = crescent.option(str, "Заголовок")
    description = crescent.option(str, "Немного о выступлении")
    character_id = crescent.option(int, "ID персонажа")
    perfomance_id = crescent.option(str, "ID сообщения начала представления")
    perfomance_channel = crescent.option(hikari.GuildTextChannel, "Канал, куда постить")

    async def callback(self, ctx: crescent.Context) -> None:
        as_url = f"https://discord.com/channels/{ctx.guild_id}/{self.perfomance_channel.id}/{self.perfomance_id}"
        view = PerfomanceView(perfomance_id=int(self.perfomance_id))
        await plugin.client.app.rest.create_message(
            self.perfomance_channel.id,
            component=PerfomancePresenter.present(
                title=self.title,
                description=self.description,
                url=as_url,
                character_id=self.character_id,
                perfomance_id=self.perfomance_id,
            ),
            flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        )
        plugin.model.component_client.start_view(view)
        await ctx.respond("posted", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def on_perfomance_review(event: hikari.ComponentInteractionCreateEvent, usecase: Inject[PerfomanceVoteUseCase]) -> None:
    if event.interaction.type != InteractionType.MESSAGE_COMPONENT:
        return

    if not all(event.interaction.custom_id.startswith(start_id) for start_id in ID_STARTS):
        return

    text_component = event.interaction.message.components[-1]
    assert isinstance(text_component, hikari.impl.TextDisplayComponentBuilder)

    character_id = int(text_component.content.split(":")[-1])
    interaction_id = event.interaction.custom_id.split("_")[0]

    await usecase.vote(
        character_id=CharacterId(character_id),
        voted_by=UserId(event.interaction.user.id),
        now=datetime.now(),
        reputation=ID_STARTS[interaction_id],
        perfomance_id=event.interaction.message.id,
    )
