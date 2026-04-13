import pytest

from marionette.application.protocols import UserId
from marionette.presentation.discord.ui.onboarding.dispatcher import OnboardingActionDispatcher
from marionette.presentation.discord.ui.onboarding.registry import OnboardingAction


class SpyUseCase:
    def __init__(self) -> None:
        self.calls: list[tuple[int, UserId]] = []

    async def execute(self, zone_id: int, user_id: UserId) -> None:
        self.calls.append((zone_id, user_id))


@pytest.mark.asyncio
async def test_onboarding_dispatcher_routes_action_to_matching_usecase() -> None:
    intro_usecase = SpyUseCase()
    rules_usecase = SpyUseCase()
    accept_rules_usecase = SpyUseCase()
    complete_usecase = SpyUseCase()
    dispatcher = OnboardingActionDispatcher(
        intro_usecase=intro_usecase,  # type: ignore[arg-type]
        rules_usecase=rules_usecase,  # type: ignore[arg-type]
        accept_rules_usecase=accept_rules_usecase,  # type: ignore[arg-type]
        complete_usecase=complete_usecase,  # type: ignore[arg-type]
    )

    await dispatcher.execute(OnboardingAction.ACCEPT_RULES, 777, UserId(100))

    assert intro_usecase.calls == []
    assert rules_usecase.calls == []
    assert accept_rules_usecase.calls == [(777, UserId(100))]
    assert complete_usecase.calls == []
