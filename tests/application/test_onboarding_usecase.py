from types import SimpleNamespace
from typing import cast

import pytest

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState, OnboardingStep
from tests.fakes import FakeTransaction


class SpyAccessManager:
    def __init__(self) -> None:
        self.calls: list[tuple[int, UserId, OnboardingStep]] = []

    async def add_role(self, zone_id: int, user_id: UserId, role_id: object) -> None:
        return None

    async def remove_role(self, zone_id: int, user_id: UserId, role_id: object) -> None:
        return None

    async def apply_step_assets(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        self.calls.append((zone_id, user_id, step))


class FakeOnboardingRepository:
    def __init__(self, state: OnboardingState | None) -> None:
        self.state = state
        self.logged_events: list[OnboardingEvent] = []

    async def get_by_user_id(self, user_id: int) -> OnboardingState | None:
        return self.state

    def add(self, state: OnboardingState) -> None:
        self.state = state

    async def log_event(self, event: OnboardingEvent) -> None:
        self.logged_events.append(event)


@pytest.mark.asyncio
async def test_move_to_updates_state_and_applies_access_assets(
    fake_transaction: FakeTransaction,
) -> None:
    state = cast(OnboardingState, SimpleNamespace(current_step=OnboardingStep.WELCOME))
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await OnboardingUseCase(repository, fake_transaction, access).move_to(
        zone_id=777,
        user_id=UserId(100),
        step=OnboardingStep.INTRO,
    )

    assert state.current_step == OnboardingStep.INTRO
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.INTRO
    assert access.calls == [(777, UserId(100), OnboardingStep.INTRO)]
