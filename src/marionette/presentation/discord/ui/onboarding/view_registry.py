import miru

from marionette.presentation.discord.ui.onboarding.registry import OnboardingRegistry


class OnboardingViewRegistry:
    def __init__(self, component_client: miru.Client) -> None:
        self._component_client = component_client

    def register_persistent_views(self, registry: OnboardingRegistry) -> None:
        for view in registry.iter_persistent_views():
            self._component_client.start_view(view, bind_to=None)
