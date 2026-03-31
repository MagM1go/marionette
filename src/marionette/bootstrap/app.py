import crescent
import hikari
import miru
from dishka import make_async_container

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.providers.db_provider import DatabaseProvider
from marionette.bootstrap.di.providers.infra_provider import InfrastructureProvider
from marionette.bootstrap.di.providers.repository_provider import RepositoryProvider
from marionette.bootstrap.di.providers.usecases_provider import UseCaseProvider


def build_discord_bot(plugins_path: str) -> hikari.GatewayBot:
    bot = hikari.GatewayBot(token=config.discord.bot_token, intents=hikari.Intents.ALL)
    dishka_container = make_async_container(
        DatabaseProvider(), InfrastructureProvider(), UseCaseProvider(), RepositoryProvider()
    )
    miru_client = miru.Client(bot)

    client = crescent.Client(
        bot,
        model=CrescentContainer(dishka_container, miru_client),
    )
    client.plugins.load_folder(plugins_path, strict=False)

    return bot
