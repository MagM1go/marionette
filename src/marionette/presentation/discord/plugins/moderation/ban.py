import crescent
import hikari

from marionette.application.protocols.types import CharacterId
from marionette.application.usecases.moderation.ban_character_usecase import BanCharacterUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(name="ban", description="Исключение персонажа из РП", guild=config.discord.main_guild_id)
class BanCommand:
    character_id = crescent.option(int, "идентификатор персонажа")

    @inject(lambda: plugin.model.dishka())
    async def callback(self, context: crescent.Context, usecase: Inject[BanCharacterUseCase]) -> None:
        await usecase.ban(CharacterId(self.character_id))
        await context.respond(f"{self.character_id} забанен")
