import hikari
import miru

from marionette.presentation.discord.exceptions import DmsNotAllowed
from marionette.presentation.discord.plugins.onboarding.steps import ONBOARDING_HELLO_CUSTOM_ID

hello_view = miru.View(timeout=None)


class HelloButton(miru.Button):
    def __init__(self) -> None:
        super().__init__("Пройти", emoji="👋", custom_id=ONBOARDING_HELLO_CUSTOM_ID)

    async def callback(self, context: miru.ViewContext) -> None:
        if context.guild_id is None:
            raise DmsNotAllowed()

        await context.respond("Удачи.", flags=hikari.MessageFlag.EPHEMERAL)
