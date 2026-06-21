import crescent
import hikari

from marionette.application.protocols.types import CharacterId
from marionette.application.usecases.moderation.approve_character_usecase import ApproveCharacterUseCase
from marionette.application.usecases.moderation.decline_character_usecase import DeclineCharacterUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.exceptions import DmsNotAllowed, InsufficientPermissions, MemberNotFound
from marionette.presentation.discord.presenters.judge_presenter import JudgePresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@plugin.include
@crescent.command(name="approve", description="Принять анкету персонажа", guild=config.discord.main_guild_id)
class ApproveCommand:
    user_id = crescent.option(hikari.User, "пользователь, чьего персонажа принимаем")
    character_id = crescent.option(int, "идентификатор персонажа")

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[ApproveCharacterUseCase]) -> None:
        if context.guild is None:
            raise DmsNotAllowed()
            
        if context.member is None or config.discord.moderator_role_id not in context.member.role_ids:
            raise InsufficientPermissions()

        character_owner = context.guild.get_member(self.user_id)
        if character_owner is None:
            raise MemberNotFound()
            
        if (amplua_role := config.discord.amplua_role_id) not in character_owner.role_ids:
            await character_owner.add_role(amplua_role, reason=f"Approved by moderator ({context.user.id})")
            
        await usecase.approve(CharacterId(self.character_id))
        await context.respond(JudgePresenter.approved())


@plugin.include
@crescent.command(name="decline", description="Отказать анкету персонажа", guild=config.discord.main_guild_id)
class DeclineCommand:
    character_id = crescent.option(int, "идентификатор персонажа")

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[DeclineCharacterUseCase]) -> None:
        if context.member is None or config.discord.moderator_role_id not in context.member.role_ids:
            raise InsufficientPermissions()

        await usecase.decline(CharacterId(self.character_id))
        await context.respond(JudgePresenter.declined())
