import typing as t
from collections.abc import Sequence

import hikari
import miru

from marionette.presentation.discord.presenters.onboarding.faq_presenter import FaqPresenter
from marionette.presentation.discord.ui.onboarding.steps import ONBOARDING_FAQ_CUSTOM_ID

_FAQ_OPTIONS: t.Final[Sequence[miru.SelectOption]] = [
    miru.SelectOption(label="Как начать?", value="start"),
    miru.SelectOption(label="Какой лор?", value="lore"),
]


class FaqView(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.text_select(placeholder="Выбери свой вопрос", options=_FAQ_OPTIONS, custom_id=ONBOARDING_FAQ_CUSTOM_ID)
    async def frequently_asked_questions(
        self, context: miru.ViewContext, select: miru.TextSelect
    ) -> None:
        match select.values[0]:
            case "start":
                text = FaqPresenter.how_to_start()
            case "lore":
                text = FaqPresenter.lore()

        await context.respond(text, flags=hikari.MessageFlag.EPHEMERAL)
