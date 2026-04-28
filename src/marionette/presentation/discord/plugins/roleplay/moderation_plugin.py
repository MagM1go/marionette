from contextlib import suppress

import crescent
import hikari

from marionette.application.protocols.roleplay_moderation_protocol import RoleplayModeration
from marionette.application.protocols.types import LocationId
from marionette.application.usecases.delete_offtopic_message_usecase import DeleteOfftopicMessageUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def message_create_event(
    event: hikari.GuildMessageCreateEvent,
    moderation_usecase: Inject[DeleteOfftopicMessageUseCase],
    moderation_service: Inject[RoleplayModeration],
) -> None:
    """Нужно для отcлеживания нахождения игрока в РП канале

    Если игрок пытается писать что-либо в РП канал, при этом НЕ находясь в нём (/entrance) - сообщения игрока будут удаляться
    Удаляться они будут при условии, если префикс не сопадает: //
    """
    if not event.is_human:
        return

    if not await moderation_service.is_rp_location(LocationId(event.channel_id)):
        return

    if await moderation_usecase.execute(
        user_id=event.author_id, channel_id=event.channel_id, message_content=event.message.content
    ):
        with suppress(hikari.NotFoundError):
            await plugin.app.rest.delete_message(channel=event.channel_id, message=event.message_id)


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
