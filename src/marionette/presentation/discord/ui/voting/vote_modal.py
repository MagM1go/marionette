from collections.abc import Sequence
from datetime import UTC, datetime

import hikari
import miru
from miru.context.modal import ModalContext

from marionette.application.protocols.types import UserId
from marionette.application.usecases.vote_usecase import VoteUseCase
from marionette.presentation.discord.presenters.vote_presenter import VotePresenter
from marionette.presentation.discord.ui.wrapper.modal_v2 import ModalV2
from marionette.presentation.discord.ui.wrapper.string_select_menu import StringSelect


class VoteModal(ModalV2):
    def __init__(self, usecase: VoteUseCase, user_id: int, character_author: UserId, character_names: Sequence[str]) -> None:
        super().__init__("Голосовалка", custom_id=f"vote_window_{user_id}", timeout=120)
        self.usecase = usecase
        self.user_id = user_id
        self.author = character_author

        # !!! ТРЕВОГА ТРЕВОГА ТРЕВОГА !!!
        self._children.append(StringSelect(label="Персонажи", options=[miru.SelectOption(label=name) for name in character_names]))

    async def callback(self, context: ModalContext) -> None:
        if self._timeout_task and self._timeout_task.cancelled():
            return

        character_name = next(iter(context.values.values()))
        self.chosen = character_name
        await self.usecase.vote_for(UserId(context.user.id), self.author, character_name, datetime.now(UTC))
        await context.respond(VotePresenter.present(character_name), flags=hikari.MessageFlag.EPHEMERAL)
