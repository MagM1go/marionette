import typing as t

import crescent
import hikari

from marionette.application.protocols import ICharacterRepository
from marionette.infrastructure.config import config
from marionette.presentation.di.inject import Inject, inject

if t.TYPE_CHECKING:
    from marionette.presentation.di.container import CrescentContainer


plugin = crescent.Plugin[hikari.GatewayBot, "CrescentContainer"]()

NON_RP_PREFIX: t.Final[str] = "//"


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def message_create_event(
    event: hikari.GuildMessageCreateEvent, character_repo: Inject[ICharacterRepository]
) -> None:
    """Нужно для отлеживания нахождения игрока в РП канале

    Если игрок пытается писать что-либо в РП канал, при этом НЕ находясь в нём (/entrance) - сообщения игрока будут удаляться
    Удаляться они будут при условии, если префикс не сопадает: //
    """
    if not event.is_human:
        return

    entranced_character = await character_repo.get_entranced_character_by_user_id(
        event.author_id
    )
    if (
        not entranced_character
        or entranced_character.entranced_channel_id == event.channel_id
    ):
        return

    message_channel = (
        plugin.app.cache.get_guild_channel(event.channel_id)
        or await event.message.fetch_channel()
    )
    if not isinstance(
        message_channel, (hikari.GuildTextChannel, hikari.GuildThreadChannel)
    ):
        return

    if not message_channel or not message_channel.parent_id:
        return

    parent = plugin.app.cache.get_guild_channel(message_channel.parent_id)
    if parent and parent.parent_id:
        parent = plugin.app.cache.get_guild_channel(parent.parent_id)

    if parent and parent.id not in config.RP_CATEGORIES:
        return

    if event.message.content and not event.message.content.startswith(NON_RP_PREFIX):
        await plugin.app.rest.delete_message(
            channel=event.channel_id, message=event.message_id
        )


@plugin.include
@crescent.event
async def on_started(_: hikari.StartedEvent) -> None:
    guild = await plugin.app.rest.fetch_guild(config.MAIN_GUILD_ID)
    threads = await plugin.app.rest.fetch_active_threads(guild)

    for thread in threads:
        channel = plugin.app.cache.get_guild_channel(thread.parent_id)
        if channel and channel.parent_id in config.RP_CATEGORIES:
            await plugin.app.rest.join_thread(thread.id)


@plugin.include
@crescent.event
async def on_thread_create(event: hikari.GuildThreadCreateEvent) -> None:
    await plugin.app.rest.join_thread(event.thread_id)
