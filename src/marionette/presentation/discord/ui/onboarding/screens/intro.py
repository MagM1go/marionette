import hikari
import miru

from marionette.presentation.discord.exceptions import DmsNotAllowed
from marionette.presentation.discord.ui.onboarding.steps import (
    ONBOARDING_INTRO_CUSTOM_ID_ABOUT,
    ONBOARDING_INTRO_CUSTOM_ID_NEXT,
)


class IntroView(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button("Что это?", custom_id=ONBOARDING_INTRO_CUSTOM_ID_ABOUT)
    async def onboarding_intro_button_about(self, context: miru.ViewContext, _: miru.Button) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        await context.respond("ну вот это", flags=hikari.MessageFlag.EPHEMERAL)
        
    @miru.button("Особенности", custom_id="what_better")
    async def onboarding_intro_button_what_better(self, context: miru.ViewContext, _: miru.Button) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        await context.respond("ну вот это", flags=hikari.MessageFlag.EPHEMERAL)
        
    @miru.button("Что дальше?", custom_id="what_next")
    async def onboarding_intro_button_next(self, context: miru.ViewContext, _: miru.Button) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        view = miru.View()
        view.add_item(NextButton())
        await context.respond("ну вот это", flags=hikari.MessageFlag.EPHEMERAL, components=view)


class NextButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(label="Дальше", custom_id=ONBOARDING_INTRO_CUSTOM_ID_NEXT)

    async def callback(self, context: miru.ViewContext) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        await context.respond("ого", flags=hikari.MessageFlag.EPHEMERAL)
