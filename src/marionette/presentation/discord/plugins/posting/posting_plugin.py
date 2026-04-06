import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.presentation.discord.plugins.posting.ui.modals.posting_modal import (
    PostBreakingNewsModal,
)

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    guild=config.discord.main_guild_id,
    name="breaking",
    description="Опубликовать важное сообщение (staff only)",
    default_member_permissions=hikari.Permissions.MANAGE_MESSAGES,
)
class BreakingNewsCommand:
    title = crescent.option(str, "Заголовок новости", max_length=45)
    source = crescent.option(
        str,
        "Выбор, из какого источника новость",
        choices=[
            ("NHK", "NHK"),
            ("Asahi Shimbun", "Asahi Shimbun"),
            ("Kyodo News", "Kyodo News"),
            ("Nikkei", "Nikkei"),
            ("Yomiuri Shimbun", "Yomiuri Shimbun"),
            ("TBS", "TBS"),
            ("Japan Times", "Japan Times"),
        ],
    )

    async def callback(self, ctx: crescent.Context) -> None:
        custom_id = f"postmodal_{ctx.user.id}"
        modal = PostBreakingNewsModal(self.title, self.source, custom_id)
        await ctx.respond_with_modal(self.title, custom_id, components=modal)
        plugin.model.component_client.start_modal(modal)
