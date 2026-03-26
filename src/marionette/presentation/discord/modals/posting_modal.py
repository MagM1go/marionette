from typing import cast, override

import hikari
import miru

from marionette.infrastructure.config import config
from marionette.presentation.discord.presenters.posting_presenter import (
    PostingPresenter,
)


class PostBreakingNewsModal(miru.Modal):
    def __init__(self, title: str, source: str, custom_id: str) -> None:
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
        placeholder="https://image-hosting.domain/image.png",
    )

    @override
    async def callback(self, context: miru.ModalContext) -> None:
        message = cast(str, self.message.value)  # доверяем контракту дискорда, что сообщение будет не пустым (required=True в self.message)
        response = PostingPresenter.present(
            username=context.user.username,
            author_id=context.user.id,
            image=self.image.value,
            source=self.source,
            message=message
        )
        
        await context.client.rest.create_message(
            config.NEWS_CHANNEL_ID,
            components=response,
            flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        )
        await context.respond("Новость была отправлена! еоу...", flags=hikari.MessageFlag.EPHEMERAL)
