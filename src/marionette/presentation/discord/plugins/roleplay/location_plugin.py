import crescent
import hikari

from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.types import UserId
from marionette.application.usecases.enter_location_usecase import EnterLocationUseCase
from marionette.application.usecases.exit_usecase import ExitLocationUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.statuses import CharacterStatus
from marionette.presentation.discord.presenters.entrance_presenter import EntryExitPresenter

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
    name="enter",
    description="Войти в локацию",
    guild=config.discord.main_guild_id,
)
class EnterCommand:
    channel = crescent.option(hikari.GuildThreadChannel, "Ветка (локация)")
    character_name = crescent.option(
        str, "Имя персонажа (полное)", autocomplete=_character_autocomplete
    )

    @inject_plugin
    async def callback(
        self, context: crescent.Context, usecase: Inject[EnterLocationUseCase]
    ) -> None:
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
    async def callback(
        self, context: crescent.Context, usecase: Inject[ExitLocationUseCase]
    ) -> None:
        await usecase.exit(context.user.id, self.character_name, context.channel_id)
        await context.respond(EntryExitPresenter.exit_message)
