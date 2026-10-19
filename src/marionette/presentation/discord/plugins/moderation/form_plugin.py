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
@crescent.command(name="approve", description="Принять анкету персонажа", guild=config.discord.guild.main)
class ApproveCommand:
    user_id = crescent.option(hikari.User, "пользователь, чьего персонажа принимаем")
    character_id = crescent.option(int, "идентификатор персонажа")
    biography = crescent.option(str, "биография персонажа (айди сообщений с био, через запятую)")

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[ApproveCharacterUseCase]) -> None:
        if context.guild is None:
            raise DmsNotAllowed()
            
        if context.member is None or config.discord.roles.moderator not in context.member.role_ids:
            raise InsufficientPermissions()

        character_owner = context.guild.get_member(self.user_id)
        if character_owner is None:
            raise MemberNotFound()
            
        if (amplua_role := config.discord.roles.amplua) not in character_owner.role_ids:
            await character_owner.add_role(amplua_role, reason=f"Approved by moderator ({context.user.id})")
            await character_owner.remove_role(config.discord.roles.unregistered, reason=f"Approved by moderator ({context.user.id})")

        ids = list(map(int, self.biography.split(",")))
        messages_content: list[str] = [(await context.channel.fetch_message(id)).content for id in ids]  # type: ignore
        await usecase.approve(CharacterId(self.character_id), "\n".join(messages_content))
        await context.respond(JudgePresenter.approved())


@plugin.include
@crescent.command(name="decline", description="Отказать анкету персонажа", guild=config.discord.guild.main)
class DeclineCommand:
    character_id = crescent.option(int, "идентификатор персонажа")

    @inject_plugin
    async def callback(self, context: crescent.Context, usecase: Inject[DeclineCharacterUseCase]) -> None:
        if context.member is None or config.discord.roles.moderator not in context.member.role_ids:
            raise InsufficientPermissions()

        await usecase.decline(CharacterId(self.character_id))
        await context.respond(JudgePresenter.declined())
