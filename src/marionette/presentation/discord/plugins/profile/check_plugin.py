import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.usecases.profile.summary_usecase import ProfileSummaryUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.plugins.profile.profile_group import profile_group
from marionette.presentation.discord.presenters.profile_presenter import ProfilePresenter
from marionette.presentation.discord.ui.profile.character_dropdown import ProfileCheckCharacterDropdown

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@profile_group.child
@crescent.command(guild=config.discord.main_guild_id, name="check", description="Посмотреть профиль пользователя")
class ProfileCheckCommand:
    user = crescent.option(hikari.User, "пользователь")

    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context, usecase: Inject[ProfileSummaryUseCase]) -> None:
        summary = await usecase.summary(user_id=UserId(self.user.id))

        if summary.characters:
            profile_view = ProfileCheckCharacterDropdown(summary)
            await ctx.respond(
                embed=ProfilePresenter.present(ctx.user.id, ctx.user.make_avatar_url(), self.user.username, summary=summary), components=profile_view
            )
            plugin.model.component_client.start_view(profile_view)
        else:
            await ctx.respond(embed=ProfilePresenter.present(ctx.user.id, ctx.user.make_avatar_url(), self.user.username, summary=summary))
