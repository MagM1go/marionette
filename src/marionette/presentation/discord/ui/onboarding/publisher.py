import hikari

from marionette.presentation.discord.ui.onboarding.registry import OnboardingScreen


class OnboardingPublisher:
    def __init__(self, rest: hikari.api.RESTClient) -> None:
        self._rest = rest

    async def publish(self, screen: OnboardingScreen) -> None:
        view = screen.create_view()
        if view is None:
            await self._rest.create_message(channel=screen.channel_id, content=screen.present())
            return

        await self._rest.create_message(
            channel=screen.channel_id,
            content=screen.present(),
            components=view,
        )
