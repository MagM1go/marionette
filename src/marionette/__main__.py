import crescent
import hikari
import miru
from dishka import make_async_container

from marionette.infrastructure.config import config
from marionette.presentation.di.container import CrescentContainer
from marionette.presentation.di.db_provider import ApplicationProvider

bot = hikari.GatewayBot(token=config.MARIONETTE_TOKEN, intents=hikari.Intents.ALL)
dishka_container = make_async_container(ApplicationProvider())
miru_client = miru.Client(bot)

client = crescent.Client(
    bot,
    model=CrescentContainer(dishka_container, miru_client),
)
client.plugins.load_folder("src.marionette.presentation.discord.plugins")

bot.run()
