from datetime import UTC, datetime

import pytest

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.accept_onboarding_rules_usecase import (
    AcceptOnboardingRulesUseCase,
)
from marionette.application.usecases.onboarding.complete_onboarding_usecase import (
    CompleteOnboardingUseCase,
)
from marionette.application.usecases.onboarding.move_onboarding_to_intro_usecase import (
    MoveOnboardingToIntroUseCase,
)
from marionette.application.usecases.onboarding.move_onboarding_to_rules_usecase import (
    MoveOnboardingToRulesUseCase,
)
from marionette.application.usecases.onboarding.start_onboarding_usecase import (
    StartOnboardingUseCase,
)
from marionette.domain.entities.onboarding import OnboardingState, OnboardingStep
from marionette.domain.exceptions import (
    OnboardingNotFoundError,
    OnboardingRulesAlreadyAcceptedError,
    OnboardingTransitionError,
)
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

    await StartOnboardingUseCase(repository, fake_transaction, access).execute(
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

    await StartOnboardingUseCase(repository, fake_transaction, access).execute(
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

    await StartOnboardingUseCase(repository, fake_transaction, access).execute(
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
async def test_move_to_intro_updates_state_and_applies_access_assets(
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

    await MoveOnboardingToIntroUseCase(repository, fake_transaction, access).execute(
        zone_id=777,
        user_id=UserId(100),
    )

    assert state.current_step == OnboardingStep.INTRO
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.INTRO
    assert access.calls == [(777, UserId(100), OnboardingStep.INTRO)]


@pytest.mark.asyncio
async def test_move_to_rules_updates_state_and_applies_access_assets(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.INTRO,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await MoveOnboardingToRulesUseCase(repository, fake_transaction, access).execute(
        zone_id=777,
        user_id=UserId(100),
    )

    assert state.current_step == OnboardingStep.RULES
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.RULES
    assert access.calls == [(777, UserId(100), OnboardingStep.RULES)]


@pytest.mark.asyncio
async def test_accept_rules_moves_state_and_applies_access_assets(
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime.now(UTC)
    state = OnboardingState(
        user_id=100,
        current_step=OnboardingStep.RULES,
        is_complete=False,
        created_at=now,
        updated_at=now,
    )
    repository = FakeOnboardingRepository(state)
    access = SpyAccessManager()

    await AcceptOnboardingRulesUseCase(repository, fake_transaction, access).execute(
        zone_id=777,
        user_id=UserId(100),
    )

    assert state.current_step == OnboardingStep.REGISTRATION
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.REGISTRATION
    assert access.calls == [(777, UserId(100), OnboardingStep.REGISTRATION)]


@pytest.mark.asyncio
async def test_complete_onboarding_marks_state_as_completed(
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

    await CompleteOnboardingUseCase(repository, fake_transaction, access).execute(
        zone_id=777,
        user_id=UserId(100),
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
async def test_move_to_intro_raises_when_onboarding_state_is_missing(
    fake_transaction: FakeTransaction,
) -> None:
    repository = FakeOnboardingRepository(None)
    access = SpyAccessManager()

    with pytest.raises(OnboardingNotFoundError):
        await MoveOnboardingToIntroUseCase(repository, fake_transaction, access).execute(
            zone_id=777,
            user_id=UserId(100),
        )

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_move_to_rules_rolls_back_for_invalid_transition(
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
        await MoveOnboardingToRulesUseCase(repository, fake_transaction, access).execute(
            zone_id=777,
            user_id=UserId(100),
        )

    assert state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_accept_rules_raises_when_rules_are_already_accepted(
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

    with pytest.raises(OnboardingRulesAlreadyAcceptedError):
        await AcceptOnboardingRulesUseCase(repository, fake_transaction, access).execute(
            zone_id=777,
            user_id=UserId(100),
        )

    assert state.current_step == OnboardingStep.REGISTRATION
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_complete_onboarding_is_idempotent_when_state_is_already_completed(
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

    await CompleteOnboardingUseCase(repository, fake_transaction, access).execute(
        zone_id=777,
        user_id=UserId(100),
    )

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 0
    assert repository.logged_events == []
    assert access.calls == []


@pytest.mark.asyncio
async def test_accept_rules_raises_when_button_is_pressed_after_completion(
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

    with pytest.raises(OnboardingRulesAlreadyAcceptedError):
        await AcceptOnboardingRulesUseCase(repository, fake_transaction, access).execute(
            zone_id=777,
            user_id=UserId(100),
        )

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
    assert access.calls == []
