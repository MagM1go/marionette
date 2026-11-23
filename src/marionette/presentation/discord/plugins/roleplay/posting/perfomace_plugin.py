from datetime import datetime

import crescent
import hikari
from crescent.ext import tasks
from hikari.interactions import InteractionType

from marionette.application.protocols import CharacterId, UserId
from marionette.application.usecases.perfomance_obtain_usecase import PerfomanceObtainUseCase
from marionette.application.usecases.vote.perfomance_vote_usecase import PerfomanceVoteUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.plugins.roleplay.posting.posting_group import posting
from marionette.presentation.discord.presenters.perfomance_presenter import PerfomancePresenter

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
    perfomance_channel = crescent.option(hikari.GuildChannel, "Канал, куда постить")

    async def callback(self, ctx: crescent.Context) -> None:
        as_url = f"https://discord.com/channels/{ctx.guild_id}/{self.perfomance_channel.id}/{self.perfomance_id}"
        await plugin.client.app.rest.create_message(
            self.perfomance_channel.id,
            components=PerfomancePresenter.present(
                title=self.title,
                description=self.description,
                url=as_url,
                character_id=self.character_id,
                perfomance_id=int(self.perfomance_id),
            ),
            flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        )
        await ctx.respond("posted", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def on_perfomance_review(
    event: hikari.ComponentInteractionCreateEvent,
    usecase: Inject[PerfomanceVoteUseCase],
) -> None:
    if event.interaction.type != InteractionType.MESSAGE_COMPONENT:
        return

    if not any(event.interaction.custom_id.startswith(start_id) for start_id in ID_STARTS):
        return

    if event.interaction.member and config.discord.roles.amplua not in event.interaction.member.role_ids:
        await event.interaction.create_initial_response(
            response_type=hikari.ResponseType.MESSAGE_CREATE, content=PerfomancePresenter.present_unregistered(), flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    text_component = next(
        component
        for component in event.interaction.message.components
        if isinstance(component, hikari.TextDisplayComponent) and "Идентификатор персонажа" in component.content
    )

    character_id = int(text_component.content.split(":")[-1].strip(" *"))
    interaction_id = event.interaction.custom_id.split("_")[0]

    await usecase.vote(
        character_id=CharacterId(character_id),
        voted_by=UserId(event.interaction.user.id),
        now=datetime.now(),
        reputation=ID_STARTS[interaction_id],
        perfomance_id=event.interaction.message.id,
    )
    await event.interaction.create_initial_response(
        response_type=hikari.ResponseType.MESSAGE_CREATE,
        content=PerfomancePresenter.present_okay(),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@plugin.include
@tasks.cronjob("0 */8 * * *", on_startup=True)
@inject(lambda: plugin.model.dishka())
async def obtain_cronjob(usecase: Inject[PerfomanceObtainUseCase]) -> None:
    await usecase.obtain()
