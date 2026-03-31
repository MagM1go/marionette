import crescent
import hikari

from marionette.bootstrap.di.container import CrescentContainer
from marionette.domain.exceptions import DomainException
from marionette.presentation.discord.presenters.error_presenter import ErrorPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.catch_command(DomainException)
async def catch_command_exception(exception: DomainException, context: crescent.Context) -> None:
    await context.respond(embed=ErrorPresenter.present(exception), ephemeral=True)
