from typing import override

import hikari
import miru

from marionette.infrastructure.config import config
from marionette.presentation.discord.presenters.posting_presenter import (
    PostingPresenter,
)


class PostBreakingNewsModal(miru.Modal):
    def __init__(self, title: str, source: str, custom_id: str) -> None:
        self.title = title
        self.source = source

        super().__init__(title, custom_id=custom_id, timeout=300)

    message = miru.TextInput(
        label="Новостное сообщение",
        required=True,
        placeholder="Сегодня погиб известный писатель...",
        style=hikari.TextInputStyle.PARAGRAPH,
    )
    image = miru.TextInput(
        label="Изображение (большое)",
        required=False,
        placeholder="https://image-hosting.domain/image.png"
    )

    @override
    async def callback(self, context: miru.ModalContext) -> None:
        channel = context.client.cache.get_guild_channel(config.NEWS_CHANNEL_ID)

        if not channel or not self.message.value:
            raise ValueError

        response = PostingPresenter.present(
            username=context.user.username,
            author_id=context.user.id,
            image=self.image.value,
            source=self.source,
            message=self.message.value,
        )
        await context.client.rest.create_message(
            channel.id,
            components=response,
            flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        )
        await context.respond(
            "Новость была отправлена! еоу...", flags=hikari.MessageFlag.EPHEMERAL
        )
