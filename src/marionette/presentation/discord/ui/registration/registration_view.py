import hikari
import miru

from marionette.presentation.discord.ui.registration.register_modal import RegistrationModal


class RegistrationView(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        label="Начать регистрацию",
        style=hikari.ButtonStyle.SUCCESS,
        custom_id="registration_button",
    )
    async def start_register(self, context: miru.ViewContext, _: miru.Button) -> None:
        await context.respond_with_modal(RegistrationModal())
