import typing as t
from datetime import UTC, datetime

import hikari
import miru
from miru.abc.item import InteractiveViewItem

from marionette.application.protocols.types import UserId
from marionette.application.usecases.vote_usecase import VoteUseCase

from marionette.presentation.discord.presenters.error_presenter import ErrorPresenter


class VoteView(miru.View):
    def __init__(self, usecase: VoteUseCase, target: hikari.User, character_name: str) -> None:
        self.usecase = usecase
        self.target = target
        self.character_name = character_name
        super().__init__(timeout=60)


    @t.override
    async def on_error(
        self,
        error: Exception,
        item: InteractiveViewItem,
        context: miru.ViewContext,
        /,
    ) -> None:
        await super().on_error(error, item, context)
        await context.respond(ErrorPresenter.present(error), flags=hikari.MessageFlag.EPHEMERAL)

    @miru.button(label="Проголосовать")
    async def vote_button(self, context: miru.ViewContext, _: miru.Button) -> None:
        await self.usecase.vote_for(
            UserId(context.author.id),
            UserId(self.target.id),
            self.character_name,
            datetime.now(UTC),
        )
        await context.respond(
            f"Вы отдали свой голос за **{self.character_name}**. Надейся, что не подведёт."
        )
