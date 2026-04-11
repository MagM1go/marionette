from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field

import hikari
import miru

from marionette.bootstrap.config import config
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.presenters.onboarding.faq_presenter import FaqPresenter
from marionette.presentation.discord.presenters.onboarding.hello_presenter import HelloPresenter
from marionette.presentation.discord.presenters.onboarding.intro_presenter import IntroPresenter
from marionette.presentation.discord.presenters.onboarding.registration_presenter import (
    RegistrationPresenter,
)
from marionette.presentation.discord.presenters.onboarding.rules_presenter import RulesPresenter
from marionette.presentation.discord.ui.onboarding.screens.faq import FaqView
from marionette.presentation.discord.ui.onboarding.screens.hello import HelloView
from marionette.presentation.discord.ui.onboarding.screens.intro import IntroView
from marionette.presentation.discord.ui.onboarding.screens.rules import RulesView
from marionette.presentation.discord.ui.onboarding.steps import (
    ONBOARDING_HELLO_CUSTOM_ID,
    ONBOARDING_INTRO_CUSTOM_ID_NEXT,
    ONBOARDING_REGISTRATION_CUSTOM_ID,
    ONBOARDING_RULES_CUSTOM_ID_ACCEPT,
)

type ScreenPresenter = (
    FaqPresenter | HelloPresenter | IntroPresenter | RulesPresenter | RegistrationPresenter
)
type ViewFactory = Callable[[], miru.View]


@dataclass(frozen=True, slots=True)
class OnboardingScreen:
    screen_id: str
    channel_id: hikari.Snowflakeish
    presenter: type[ScreenPresenter]
    view_factory: ViewFactory | None = None
    custom_id_to_step: Mapping[str, OnboardingStep] = field(default_factory=dict)

    def present(self) -> str:
        return self.presenter.present()

    def create_view(self) -> miru.View | None:
        if self.view_factory is None:
            return None

        return self.view_factory()


class OnboardingRegistry:
    def __init__(self, screens: Sequence[OnboardingScreen]) -> None:
        self._screens = tuple(screens)
        self._screens_by_id = {screen.screen_id: screen for screen in self._screens}
        self._target_steps_by_custom_id = {
            custom_id: step
            for screen in self._screens
            for custom_id, step in screen.custom_id_to_step.items()
        }

    @property
    def screens(self) -> tuple[OnboardingScreen, ...]:
        return self._screens

    def get_by_id(self, id: str) -> OnboardingScreen | None:
        return self._screens_by_id.get(id)

    def get_target_step(self, custom_id: str) -> OnboardingStep | None:
        return self._target_steps_by_custom_id.get(custom_id)

    def iter_persistent_views(self) -> tuple[miru.View, ...]:
        return tuple(view for screen in self._screens if (view := screen.create_view()) is not None)


onboarding_registry = OnboardingRegistry(
    screens=(
        OnboardingScreen(
            screen_id="hello",
            channel_id=config.discord.onboarding_welcome_channel_id,
            presenter=HelloPresenter,
            view_factory=HelloView,
            custom_id_to_step={ONBOARDING_HELLO_CUSTOM_ID: OnboardingStep.INTRO},
        ),
        OnboardingScreen(
            screen_id="intro",
            channel_id=config.discord.onboarding_intro_channel_id,
            presenter=IntroPresenter,
            view_factory=IntroView,
            custom_id_to_step={ONBOARDING_INTRO_CUSTOM_ID_NEXT: OnboardingStep.RULES},
        ),
        OnboardingScreen(
            screen_id="rules",
            channel_id=config.discord.onboarding_rules_channel_id,
            presenter=RulesPresenter,
            view_factory=RulesView,
            custom_id_to_step={ONBOARDING_RULES_CUSTOM_ID_ACCEPT: OnboardingStep.REGISTRATION},
        ),
        OnboardingScreen(
            screen_id="faq",
            channel_id=config.discord.onboarding_faq_channel_id,
            presenter=FaqPresenter,
            view_factory=FaqView,
        ),
        OnboardingScreen(
            screen_id="registration",
            channel_id=config.discord.registration_channel_id,
            presenter=RegistrationPresenter,
            custom_id_to_step={ONBOARDING_REGISTRATION_CUSTOM_ID: OnboardingStep.COMPLETED},
        ),
    )
)
