import hikari
import miru
from miru.context import ViewContext
from miru.ext import nav

from marionette.application.usecases.profile.summary_usecase import SummaryData
from marionette.presentation.discord.presenters.profile_presenter import ProfilePresenter


class BiographyButton(nav.NavButton):
    def __init__(self, biographies: dict[int, list[hikari.Embed]]) -> None:
        super().__init__("Биография")

        self.biographies = biographies

    async def callback(self, context: ViewContext, /) -> None:
        navigator = nav.NavigatorView(pages=self.biographies[self.view.current_page])

        builder = await navigator.build_response_async(context.client)
        builder.set_flags(hikari.MessageFlag.EPHEMERAL)
        await builder.create_initial_response(context.interaction)

        context.client.start_view(navigator)

    async def before_page_change(self) -> None:
        self.view._children[-1] = self


class ProfileCheckCharacterTextSelect(miru.TextSelect):
    def __init__(self, options: list[miru.SelectOption], summary: SummaryData) -> None:
        super().__init__(options=options)

        self.summary = summary

    async def callback(self, context: ViewContext, /) -> None:
        character_index = next(i for i in range(len(self.summary.characters)) if self.summary.characters[i].name == self.values[0])

        pages = ProfilePresenter.present_character_pages(self.summary.characters)
        character_biographies = {i: ProfilePresenter.present_character_biography_pages(self.summary.characters[i]) for i in range(len(self.summary.characters))}

        navigator = nav.NavigatorView(pages=pages)
        navigator.add_item(BiographyButton(character_biographies))

        builder = await navigator.build_response_async(context.client, start_at=character_index)
        builder.set_flags(hikari.MessageFlag.EPHEMERAL)
        await builder.create_initial_response(context.interaction)

        context.client.start_view(navigator)


class ProfileCheckCharacterDropdown(miru.View):
    def __init__(self, summary: SummaryData) -> None:
        super().__init__()

        self.add_item(ProfileCheckCharacterTextSelect([miru.SelectOption(label=c.name) for c in summary.characters], summary))
