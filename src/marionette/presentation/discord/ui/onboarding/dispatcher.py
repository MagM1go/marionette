from collections.abc import Awaitable, Callable

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.accept_onboarding_rules_usecase import AcceptOnboardingRulesUseCase
from marionette.application.usecases.onboarding.complete_onboarding_usecase import CompleteOnboardingUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_intro_usecase import MoveOnboardingToIntroUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_rules_usecase import MoveOnboardingToRulesUseCase
from marionette.presentation.discord.ui.onboarding.registry import OnboardingAction

type OnboardingActionHandler = Callable[[int, UserId], Awaitable[None]]


class OnboardingActionDispatcher:
    def __init__(
        self,
        intro_usecase: MoveOnboardingToIntroUseCase,
        rules_usecase: MoveOnboardingToRulesUseCase,
        accept_rules_usecase: AcceptOnboardingRulesUseCase,
        complete_usecase: CompleteOnboardingUseCase,
    ) -> None:
        self._handlers: dict[OnboardingAction, OnboardingActionHandler] = {
            OnboardingAction.GO_TO_INTRO: intro_usecase.execute,
            OnboardingAction.GO_TO_RULES: rules_usecase.execute,
            OnboardingAction.ACCEPT_RULES: accept_rules_usecase.execute,
            OnboardingAction.COMPLETE: complete_usecase.execute,
        }

    async def execute(self, action: OnboardingAction, zone_id: int, user_id: UserId) -> None:
        await self._handlers[action](zone_id, user_id)
