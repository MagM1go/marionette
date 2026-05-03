import crescent
import hikari

from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.presenters.paparazzi_presenter import PaparazziPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


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

    entered_character = await character_repo.get_entered_character_by_user_id(
        UserId(event.author_id)
    )

    if not entered_character:
        return

    if not entered_character.entered_channel_id:
        return

    channel = plugin.app.cache.get_guild_channel(event.channel_id) or plugin.app.cache.get_thread(
        event.channel_id
    )
    if not channel or not channel.name:
        return

    if not channel.name.startswith(config.discord.paparazzi_trigger_channel_prefix):
        return

    result = await paparazzi_usecase.expose(entered_character)
    if result:
        response = PaparazziPresenter.present(
            channel_id=entered_character.entered_channel_id,
            character_name=entered_character.name,
        )
        await event.app.rest.create_message(
            channel=config.discord.tabloid_channel_id, embed=response
        )
