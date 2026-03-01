import typing as t

import crescent
import hikari

from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.application.usecases.expose_usecase import ExposeCharacterUseCase
from marionette.discord.sender import send_result, send_result_with_context
from marionette.domain.repositories import ICharacterRepository
from marionette.infrastructure.config import config
from marionette.infrastructure.di.inject import Inject, inject
from marionette.presentation.result_presenter import ResultPresenter

if t.TYPE_CHECKING:
    from marionette.infrastructure.di.container import CrescentContainer

plugin = crescent.Plugin[hikari.GatewayBot, "CrescentContainer"]()
inject_plugin = inject(lambda: plugin.model.dishka())


@inject_plugin
async def _character_autocomplete(
    context: crescent.AutocompleteContext,
    _: hikari.AutocompleteInteractionOption,
    character_repo: Inject[ICharacterRepository],
) -> list[tuple[str, str]]:
    characters = await character_repo.get_all_characters_by_user_id(context.user.id)
    return [(c.name, c.name) for c in characters]


@plugin.include
@crescent.command(
    name="entrance",
    description="Войти в таймлайн",
    guild=config.MAIN_GUILD_ID,
)
class EntranceCommand:
    channel = crescent.option(hikari.GuildThreadChannel, "Ветка (таймлайн)")
    character_name = crescent.option(
        str, "Имя персонажа (полное)", autocomplete=_character_autocomplete
    )

    @inject_plugin
    async def callback(
        self, context: crescent.Context, usecase: Inject[EntranceUseCase]
    ) -> None:
        result = await usecase.execute(
            context.user.id, self.character_name, self.channel.id
        )
        response = ResultPresenter.present(result)
        await send_result_with_context(context, response, ephemeral=True)


@plugin.include
@crescent.command(
    name="exit",
    description="Выйти из таймлайна",
    guild=config.MAIN_GUILD_ID,
)
class ExitCommand:
    character_name = crescent.option(
        str, "Имя персонажа (полное)", autocomplete=_character_autocomplete
    )

    @inject_plugin
    async def callback(
        self, context: crescent.Context, usecase: Inject[ExitUseCase]
    ) -> None:
        result = await usecase.execute(
            context.channel_id, context.user.id, self.character_name
        )
        response = ResultPresenter.present(result)
        await send_result_with_context(context, response, ephemeral=True)


@plugin.include
@crescent.event
@inject_plugin
async def tabloid_event(
    event: hikari.MessageCreateEvent,
    character_repo: Inject[ICharacterRepository],
    expose_usecase: Inject[ExposeCharacterUseCase],
) -> None:
    if not event.is_human:
        return
        
    entranced_character = await character_repo.get_entranced_character_by_user_id(event.author_id)
    if not entranced_character:
        return

    result = await expose_usecase.expose(entranced_character)
    if result:
        response = ResultPresenter.present(result)
        await send_result(plugin.app.rest, config.TABLOID_CHANNEL_ID, response)
