import crescent
import hikari

from marionette.presentation.di.container import CrescentContainer

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
async def on_button_click(event: hikari.ComponentInteractionCreateEvent) -> None: ...
