import pytest

from marionette.application.protocols import UserId
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.ui.onboarding.dispatcher import OnboardingActionDispatcher
from marionette.presentation.discord.ui.onboarding.registry import OnboardingAction


class SpyUseCase:
    def __init__(self, result: OnboardingStep | None) -> None:
        self.result = result
        self.calls: list[UserId] = []

    async def execute(self, user_id: UserId) -> OnboardingStep | None:
        self.calls.append(user_id)
        return self.result


class SpyStepAssets:
    def __init__(self) -> None:
        self.calls: list[tuple[int, UserId, OnboardingStep]] = []

    async def apply(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        self.calls.append((zone_id, user_id, step))


@pytest.mark.asyncio
async def test_onboarding_dispatcher_routes_action_and_applies_step_assets() -> None:
    intro_usecase = SpyUseCase(None)
    rules_usecase = SpyUseCase(None)
    accept_rules_usecase = SpyUseCase(OnboardingStep.REGISTRATION)
    complete_usecase = SpyUseCase(None)
    step_assets = SpyStepAssets()
    dispatcher = OnboardingActionDispatcher(
        intro_usecase=intro_usecase,  # type: ignore[arg-type]
        rules_usecase=rules_usecase,  # type: ignore[arg-type]
        accept_rules_usecase=accept_rules_usecase,  # type: ignore[arg-type]
        complete_usecase=complete_usecase,  # type: ignore[arg-type]
        step_assets=step_assets,  # type: ignore[arg-type]
    )

    await dispatcher.execute(OnboardingAction.ACCEPT_RULES, 777, UserId(100))

    assert intro_usecase.calls == []
    assert rules_usecase.calls == []
    assert accept_rules_usecase.calls == [UserId(100)]
    assert complete_usecase.calls == []
    assert step_assets.calls == [(777, UserId(100), OnboardingStep.REGISTRATION)]


@pytest.mark.asyncio
async def test_onboarding_dispatcher_skips_step_assets_when_action_does_not_move() -> None:
    intro_usecase = SpyUseCase(None)
    rules_usecase = SpyUseCase(None)
    accept_rules_usecase = SpyUseCase(None)
    complete_usecase = SpyUseCase(None)
    step_assets = SpyStepAssets()
    dispatcher = OnboardingActionDispatcher(
        intro_usecase=intro_usecase,  # type: ignore[arg-type]
        rules_usecase=rules_usecase,  # type: ignore[arg-type]
        accept_rules_usecase=accept_rules_usecase,  # type: ignore[arg-type]
        complete_usecase=complete_usecase,  # type: ignore[arg-type]
        step_assets=step_assets,  # type: ignore[arg-type]
    )

    await dispatcher.execute(OnboardingAction.GO_TO_INTRO, 777, UserId(100))

    assert intro_usecase.calls == [UserId(100)]
    assert step_assets.calls == []
