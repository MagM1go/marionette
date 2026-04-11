from datetime import UTC, datetime

import pytest

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.domain.entities.onboarding import OnboardingState, OnboardingStep
from marionette.domain.exceptions import OnboardingNotFoundError, OnboardingTransitionError
from tests.fakes import FakeOnboardingRepository, FakeTransaction


class SpyAccessManager:
    def __init__(self) -> None:
        self.calls: list[tuple[int, UserId, OnboardingStep]] = []

    async def add_role(self, zone_id: int, user_id: UserId, role_id: object) -> None:
        return None

    async def remove_role(self, zone_id: int, user_id: UserId, role_id: object) -> None:
        return None

    async def apply_step_assets(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        self.calls.append((zone_id, user_id, step))


@pytest.mark.asyncio
async def test_start_creates_state_and_moves_to_welcome(
    fake_transaction: FakeTransaction,
) -> None:
    repository = FakeOnboardingRepository(None)
    access = SpyAccessManager()

    await OnboardingUseCase(repository, fake_transaction, access).start(
        zone_id=777,
        user_id=UserId(100),
    )

    assert repository.state is not None
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.WELCOME
    assert access.calls == [(777, UserId(100), OnboardingStep.WELCOME)]


@pytest.mark.asyncio
async def test_start_is_idempotent_for_existing_onboarding(
    fake_transaction: FakeTransaction,
) -> None:
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.WELCOME,
        is_complete=False,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await OnboardingUseCase(repository, fake_transaction, access).start(
        zone_id=777,
        user_id=UserId(100),
    )

    assert repository.state is state
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 0
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_start_moves_existing_newbie_state_to_welcome(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.NEWBIE,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await OnboardingUseCase(repository, fake_transaction, access).start(
        zone_id=777,
        user_id=UserId(100),
    )

    assert repository.state is state
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.WELCOME
    assert access.calls == [(777, UserId(100), OnboardingStep.WELCOME)]


@pytest.mark.asyncio
async def test_move_to_updates_state_and_applies_access_assets(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.WELCOME,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
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


@pytest.mark.asyncio
async def test_move_to_marks_onboarding_as_completed(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.REGISTRATION,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await OnboardingUseCase(repository, fake_transaction, access).move_to(
        zone_id=777,
        user_id=UserId(100),
        step=OnboardingStep.COMPLETED,
    )

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert state.completed_at is not None
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.COMPLETED
    assert access.calls == [(777, UserId(100), OnboardingStep.COMPLETED)]


@pytest.mark.asyncio
async def test_move_to_raises_when_onboarding_state_is_missing(
    fake_transaction: FakeTransaction,
) -> None:
    repository = FakeOnboardingRepository(None)
    access = SpyAccessManager()

    with pytest.raises(OnboardingNotFoundError):
        await OnboardingUseCase(repository, fake_transaction, access).move_to(
            zone_id=777,
            user_id=UserId(100),
            step=OnboardingStep.WELCOME,
        )

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_move_to_rolls_back_for_invalid_transition(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.WELCOME,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    with pytest.raises(OnboardingTransitionError):
        await OnboardingUseCase(repository, fake_transaction, access).move_to(
            zone_id=777,
            user_id=UserId(100),
            step=OnboardingStep.RULES,
        )

    assert state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_move_to_rolls_back_when_onboarding_is_already_completed(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.COMPLETED,
        is_complete=True,
        created_at=now,
        updated_at=now,
        completed_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    with pytest.raises(OnboardingTransitionError):
        await OnboardingUseCase(repository, fake_transaction, access).move_to(
            zone_id=777,
            user_id=UserId(100),
            step=OnboardingStep.COMPLETED,
        )

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []
