from collections.abc import Awaitable, Callable

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.accept_onboarding_rules_usecase import AcceptOnboardingRulesUseCase
from marionette.application.usecases.onboarding.complete_onboarding_usecase import CompleteOnboardingUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_intro_usecase import MoveOnboardingToIntroUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_rules_usecase import MoveOnboardingToRulesUseCase
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.ui.onboarding.registry import OnboardingAction
from marionette.presentation.discord.ui.onboarding.step_assets import OnboardingStepAssets

type OnboardingActionHandler = Callable[[UserId], Awaitable[OnboardingStep | None]]


class OnboardingActionDispatcher:
    def __init__(
        self,
        intro_usecase: MoveOnboardingToIntroUseCase,
        rules_usecase: MoveOnboardingToRulesUseCase,
        accept_rules_usecase: AcceptOnboardingRulesUseCase,
        complete_usecase: CompleteOnboardingUseCase,
        step_assets: OnboardingStepAssets,
    ) -> None:
        self._handlers: dict[OnboardingAction, OnboardingActionHandler] = {
            OnboardingAction.GO_TO_INTRO: intro_usecase.execute,
            OnboardingAction.GO_TO_RULES: rules_usecase.execute,
            OnboardingAction.ACCEPT_RULES: accept_rules_usecase.execute,
            OnboardingAction.COMPLETE: complete_usecase.execute,
        }
        self._step_assets = step_assets

    async def execute(self, action: OnboardingAction, zone_id: int, user_id: UserId) -> None:
        step = await self._handlers[action](user_id)
        if step is None:
            return

        await self._step_assets.apply(zone_id=zone_id, user_id=user_id, step=step)
