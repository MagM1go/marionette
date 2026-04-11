import hikari
import miru

from marionette.presentation.discord.exceptions import DmsNotAllowed
from marionette.presentation.discord.ui.onboarding.steps import ONBOARDING_HELLO_CUSTOM_ID


class HelloView(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button("Пройти", emoji="👋", custom_id=ONBOARDING_HELLO_CUSTOM_ID)
    async def onboarding_hello_button(self, context: miru.ViewContext, _: miru.Button) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        await context.respond("Удачи.", flags=hikari.MessageFlag.EPHEMERAL)
