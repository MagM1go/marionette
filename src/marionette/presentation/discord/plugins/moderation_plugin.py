import typing as t

import crescent
import hikari

from marionette.domain.repositories import ICharacterRepository
from marionette.infrastructure.di.inject import Inject, inject

if t.TYPE_CHECKING:
    from marionette.infrastructure.di.container import CrescentContainer


plugin = crescent.Plugin[hikari.GatewayBot, "CrescentContainer"]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def message_create_event(
    event: hikari.MessageCreateEvent, character_repo: Inject[ICharacterRepository]
) -> None:
    if not event.is_human:
        return

    entranced_character = await character_repo.get_entranced_character_by_user_id(
        event.author_id
    )
    if not entranced_character:
        return

    if not entranced_character.entranced_channel_id:
        return

    entranced_channel_id = entranced_character.entranced_channel_id
    message_channel = plugin.app.cache.get_guild_channel(entranced_channel_id)
    if not message_channel:
        return

    if not message_channel.parent_id:
        return

    category = plugin.app.cache.get_guild_channel(message_channel.parent_id)
