import crescent
import hikari

from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.usecases.enter_location_usecase import EnterLocationUseCase
from marionette.application.usecases.exit_usecase import ExitLocationUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.presenters.entrance_presenter import (
    EntryExitPresenter,
)
from marionette.presentation.discord.presenters.paparazzi_presenter import (
    PaparazziPresenter,
)

from marionette.domain.statuses import CharacterStatus

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@inject_plugin
async def _character_autocomplete(
    context: crescent.AutocompleteContext,
    _: hikari.AutocompleteInteractionOption,
    character_repo: Inject[CharacterRepository],
) -> list[tuple[str, str]]:
    characters = await character_repo.get_all_characters_by_user_id(UserId(context.user.id))
    return [(c.name, c.name) for c in characters if c.status == CharacterStatus.IS_ACTIVE]


@plugin.include
@crescent.command(
    name="entrance",
    description="Войти в локацию",
    guild=config.discord.main_guild_id,
)
class EntranceCommand:
    channel = crescent.option(hikari.GuildThreadChannel, "Ветка (таймлайн)")
    character_name = crescent.option(
        str, "Имя персонажа (полное)", autocomplete=_character_autocomplete
    )

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[EnterLocationUseCase]) -> None:
        result = await usecase.enter(context.user.id, self.character_name, self.channel.id)
        response = EntryExitPresenter.present_entry(result.location_id)
        await context.respond(response)


@plugin.include
@crescent.command(
    name="exit",
    description="Выйти с локации",
    guild=config.discord.main_guild_id,
)
class ExitCommand:
    character_name = crescent.option(
        str, "Имя персонажа (полное)", autocomplete=_character_autocomplete
    )

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[ExitLocationUseCase]) -> None:
        await usecase.exit(context.user.id, self.character_name, context.channel_id)
        await context.respond(EntryExitPresenter.exit_message)


@plugin.include
@crescent.event
@inject_plugin
async def tabloid_event(
    event: hikari.MessageCreateEvent,
    character_repo: Inject[CharacterRepository],
    paparazzi_usecase: Inject[PaparazziUseCase],
) -> None:
    if not event.is_human:
        return

    entranced_character = await character_repo.get_entranced_character_by_user_id(
        UserId(event.author_id)
    )

    if not entranced_character:
        return

    if not entranced_character.entranced_channel_id:
        return

    channel = plugin.app.cache.get_guild_channel(event.channel_id) or plugin.app.cache.get_thread(
        event.channel_id
    )
    if not channel or not channel.name:
        return

    if not channel.name.startswith(config.discord.paparazzi_trigger_channel_prefix):
        return

    result = await paparazzi_usecase.expose(entranced_character)
    if result:
        response = PaparazziPresenter.present(
            channel_id=entranced_character.entranced_channel_id,
            character_name=entranced_character.name,
        )
        await event.app.rest.create_message(channel=config.discord.tabloid_channel_id, embed=response)
