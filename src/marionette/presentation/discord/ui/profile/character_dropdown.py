import hikari
import miru
from miru.context import ViewContext
from miru.ext import nav

from marionette.application.usecases.profile.summary_usecase import SummaryData
from marionette.presentation.discord.presenters.profile_presenter import ProfilePresenter


class MyNavButton(nav.NavButton):
    async def before_page_change(self) -> None:
        self.label = f"Страница: {self.view.current_page + 1}"


class ProfileCheckCharacterTextSelect(miru.TextSelect):
    def __init__(self, options: list[miru.SelectOption], summary: SummaryData) -> None:
        super().__init__(options=options)

        self.summary = summary

    async def callback(self, context: ViewContext, /) -> None:
        biography_buttons = [
            nav.FirstButton(),
            nav.PrevButton(),
            nav.NextButton(),
            nav.LastButton(),
            nav.NavButton(label="Страница", disabled=True),
        ]
        navigator = nav.NavigatorView(pages=ProfilePresenter.present_character_pages(self.summary), items=biography_buttons)

        builder = await navigator.build_response_async(context.client)
        builder.set_flags(hikari.MessageFlag.EPHEMERAL)
        await builder.send_to_channel(context.channel_id)

        context.client.start_view(navigator)


class ProfileCheckCharacterDropdown(miru.View):
    def __init__(self, summary: SummaryData) -> None:
        super().__init__()

        self.add_item(ProfileCheckCharacterTextSelect([miru.SelectOption(label=c.name) for c in summary.characters], summary))
