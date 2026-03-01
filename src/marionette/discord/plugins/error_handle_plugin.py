import typing as t

import crescent
import hikari

from marionette.discord.sender import send_result_with_context
from marionette.domain.exceptions import DomainException

if t.TYPE_CHECKING:
    from marionette.infrastructure.di.container import CrescentContainer


plugin = crescent.Plugin[hikari.GatewayBot, "CrescentContainer"]()


@plugin.include
@crescent.catch_command(DomainException)
async def catch_command_exception(
    exception: DomainException, context: crescent.Context
) -> None:
    await send_result_with_context(context, exception.message, ephemeral=True)
