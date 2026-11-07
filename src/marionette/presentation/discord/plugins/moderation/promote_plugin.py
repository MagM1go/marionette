import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.promote_usecase import PromoteStaffUseCase
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.entities.staff import StaffRoles
from marionette.presentation.discord.presenters.promote_presenter import PromotePresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(name="promote", description="Выдать стафф-роль участнику", default_member_permissions=hikari.Permissions.ADMINISTRATOR)
class PromoteCommand:
    user = crescent.option(hikari.User, "пользователь")
    role = crescent.option(str, "выдаваемая роль", choices=[(role.name, role.name) for role in StaffRoles])

    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context, usecase: Inject[PromoteStaffUseCase]) -> None:
        await usecase.promote(user_id=UserId(self.user.id), role=StaffRoles[self.role])
        await ctx.respond(PromotePresenter.present(self.user.mention, self.role))
