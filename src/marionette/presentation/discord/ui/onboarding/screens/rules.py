import typing as t
from collections.abc import Sequence

import hikari
import miru

from marionette.presentation.discord.presenters.onboarding.rules_presenter import RulesPresenter
from marionette.presentation.discord.ui.onboarding.steps import (
    ONBOARDING_RULES_CUSTOM_ID,
    ONBOARDING_RULES_CUSTOM_ID_ACCEPT,
)

_RULES_OPTIONS: t.Final[Sequence[miru.SelectOption]] = [
    miru.SelectOption(label="Общие правила", value=RulesPresenter.general_rules())
]


class RulesView(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        "Я прочитал и принимаю правила", emoji="✅", custom_id=ONBOARDING_RULES_CUSTOM_ID_ACCEPT
    )
    async def accept_rules(self, context: miru.ViewContext, _: miru.Button) -> None:
        await context.respond("✅", flags=hikari.MessageFlag.EPHEMERAL)

    @miru.text_select(options=_RULES_OPTIONS, custom_id=ONBOARDING_RULES_CUSTOM_ID)
    async def rules(self, context: miru.ViewContext, select: miru.TextSelect) -> None:
        await context.respond(select.values[0], flags=hikari.MessageFlag.EPHEMERAL)
