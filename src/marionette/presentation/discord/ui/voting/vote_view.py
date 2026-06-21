import miru

from marionette.presentation.discord.ui.voting.vote_modal import VoteModal


class VoteView(miru.View):
    def __init__(self, modal: VoteModal) -> None:
        super().__init__(timeout=60)
        self.modal = modal

    @miru.button(label="Проголосовать")
    async def vote_button(self, context: miru.ViewContext, _: miru.Button) -> None:
        await context.respond_with_modal(modal=self.modal)
