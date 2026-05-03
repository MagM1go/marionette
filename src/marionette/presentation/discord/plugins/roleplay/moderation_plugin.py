from contextlib import suppress

import crescent
import hikari

from marionette.application.usecases.delete_offtopic_message_usecase import (
    DeleteOfftopicMessageUseCase,
)
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.helpers import get_or_fetch_channel

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def message_create_event(
    event: hikari.GuildMessageCreateEvent,
    moderation_usecase: Inject[DeleteOfftopicMessageUseCase],
) -> None:
    """Нужно для отcлеживания нахождения игрока в РП канале
    Если игрок пытается писать что-либо в РП канал, при этом НЕ находясь в нём (/enter) - сообщения игрока будут удаляться
    Удаляться они будут при условии, если префикс не сопадает: //
    """
    if not event.is_human or not event.message.content:
        return

    channel = await get_or_fetch_channel(plugin.app.rest, plugin.app.cache, event.channel_id)
    if not isinstance(channel, hikari.GuildChannel) or channel.parent_id is None:
        return

    parent = await get_or_fetch_channel(plugin.app.rest, plugin.app.cache, channel.parent_id)
    if not isinstance(parent, hikari.GuildChannel):
        return

    if parent.parent_id is not None:
        parent = await get_or_fetch_channel(plugin.app.rest, plugin.app.cache, parent.parent_id)
        if not isinstance(parent, hikari.GuildChannel):
            return

    if parent.id not in config.discord.rp_categories:
        return

    should_delete = await moderation_usecase.execute(
        user_id=event.author_id,
        channel_id=event.channel_id,
        message_content=event.message.content,
    )
    if not should_delete:
        return

    with suppress(hikari.NotFoundError, hikari.ForbiddenError):
        await plugin.app.rest.delete_message(
            channel=event.channel_id,
            message=event.message_id,
        )


@plugin.include
@crescent.event
async def on_started(_: hikari.StartedEvent) -> None:
    guild = await plugin.app.rest.fetch_guild(config.discord.main_guild_id)
    threads = await plugin.app.rest.fetch_active_threads(guild)

    for thread in threads:
        channel = plugin.app.cache.get_guild_channel(thread.parent_id)
        if channel and channel.parent_id in config.discord.rp_categories:
            await plugin.app.rest.join_thread(thread.id)


@plugin.include
@crescent.event
async def on_thread_create(event: hikari.GuildThreadCreateEvent) -> None:
    await plugin.app.rest.join_thread(event.thread_id)
