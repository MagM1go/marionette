import asyncio
from datetime import datetime

import crescent
import hikari
from dishka import make_async_container

from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles
from marionette.infrastructure.config import config
from marionette.infrastructure.db.manager import DBManager
from marionette.infrastructure.di.container import CrescentContainer
from marionette.infrastructure.di.db_provider import ApplicationProvider
from marionette.infrastructure.repositories.character_repository import (
    CharacterRepository,
)

bot = hikari.GatewayBot(token=config.MARIONETTE_TOKEN, intents=hikari.Intents.ALL)
dishka_container = make_async_container(ApplicationProvider())

client = crescent.Client(
    bot,
    model=CrescentContainer(
        dishka_container,
    ),
)
client.plugins.load_folder("src.marionette.discord.plugins")


'''async def main():
    db = DBManager(config.DATABASE_URL)

    async with db.get_session() as session:
        repo = CharacterRepository(session)
        await repo.save(
            name="Аяна",
            user_id=598387707311554570,
            role=Roles.IDOL,
            birthday=datetime.today(),
            home_channel_id=1473720774605930624
        )
'''
# asyncio.run(main())
bot.run()
