import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.moderation.report_usecase import ReportUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.exceptions import IsNotId
from marionette.presentation.discord.presenters.report_presenter import ReportPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(guild=config.discord.guild.main, name="report", description="Отправить жалобу на пользователя")
class ReportCommand:
    user = crescent.option(hikari.User, "нарушитель")
    message_id = crescent.option(str, "ID сообщения с нарушением (или начало)")
    reason = crescent.option(str, "опишите пункт нарушения / причину", min_length=12, max_length=4096)

    @inject(lambda: plugin.model.dishka())
    async def callback(self, ctx: crescent.Context, usecase: Inject[ReportUseCase]) -> None:
        if not self.message_id.isdigit():
            raise IsNotId()

        await usecase.report(UserId(ctx.user.id), UserId(self.user.id), self.reason)
        message = await ctx.respond(ReportPresenter.present(self.user.mention), user_mentions=True)
        assert message is not None
        
        await ctx.client.app.rest.create_message(
            channel=config.discord.text_channels.reports,
            embed=ReportPresenter.present_moderator_embed(
                issuer_id=ctx.user.id,
                issuer_name=ctx.user.username,
                user_id=self.user.id,
                user_name=self.user.username,
                reason=self.reason,
                report_channel_id=ctx.channel_id,
                report_message_id=message.id,
            ),
        )
