import crescent
import hikari

from marionette.bootstrap.di.container import CrescentContainer
from marionette.domain.exceptions import DomainException
from marionette.presentation.discord.exceptions import DiscordException
from marionette.presentation.discord.presenters.error_presenter import ErrorPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.catch_command(DomainException, DiscordException)
async def catch_command_exception(exception: DomainException, context: crescent.Context) -> None:
    await context.respond(embed=ErrorPresenter.present(exception), ephemeral=True)


@plugin.include
@crescent.catch_event(DomainException)
async def catch_modal_interaction_event_exception(
    exception: DomainException, event: hikari.Event
) -> None:
    if not isinstance(event, hikari.ModalInteractionCreateEvent):
        return
        
    await event.interaction.create_initial_response(
        response_type=hikari.ResponseType.MESSAGE_CREATE,
        embed=ErrorPresenter.present(exception),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
