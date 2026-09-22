import crescent
import hikari

from marionette.application.protocols.types import CharacterId, UserId
from marionette.application.queries.characters import CharacterQueries
from marionette.application.usecases.subscribe_usecase import SubscribeUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.exceptions import CharacterNotFound

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@plugin.include
@crescent.command(guild=config.discord.main_guild_id, name="subscribe", description="Начать отслеживать понравившегося автора.")
@inject_plugin
class SubscribeCommand:
    owner = crescent.option(hikari.User, "автор персонажа")
    character = crescent.option(str, "персонаж, за которой хотите следить")

    @inject_plugin
    async def callback(self, ctx: crescent.Context, character_queries: Inject[CharacterQueries], usecase: Inject[SubscribeUseCase]) -> None:
        character = await character_queries.get_character(UserId(self.owner.id), self.character)

        if not character:
            raise CharacterNotFound(self.character)

        await usecase.subscribe(UserId(ctx.user.id), UserId(self.owner.id), CharacterId(character.id))
        await ctx.respond(f"Вы подписались на, дай боже Вам сил, на **{character.name}**.", ephemeral=True)
