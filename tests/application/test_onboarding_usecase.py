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


@pytest.mark.asyncio
async def test_start_creates_state_and_moves_to_welcome(
    fake_transaction: FakeTransaction,
) -> None:
    repository = FakeOnboardingRepository(None)

    result = await StartOnboardingUseCase(repository, fake_transaction).execute(UserId(100))

    assert repository.state is not None
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.WELCOME
    assert result == OnboardingStep.WELCOME


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

    result = await StartOnboardingUseCase(repository, fake_transaction).execute(UserId(100))

    assert repository.state is state
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 0
    assert repository.logged_events == []
    assert result is None


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

    result = await StartOnboardingUseCase(repository, fake_transaction).execute(UserId(100))

    assert repository.state is state
    assert repository.state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.WELCOME
    assert result == OnboardingStep.WELCOME


@pytest.mark.asyncio
async def test_move_to_intro_updates_state_and_returns_intro_step(
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

    result = await MoveOnboardingToIntroUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.INTRO
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.INTRO
    assert result == OnboardingStep.INTRO


@pytest.mark.asyncio
async def test_move_to_rules_updates_state_and_returns_rules_step(
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

    result = await MoveOnboardingToRulesUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.RULES
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.RULES
    assert result == OnboardingStep.RULES


@pytest.mark.asyncio
async def test_accept_rules_moves_state_and_returns_registration_step(
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

    result = await AcceptOnboardingRulesUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.REGISTRATION
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.REGISTRATION
    assert result == OnboardingStep.REGISTRATION


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

    result = await CompleteOnboardingUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert state.completed_at is not None
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
    assert len(repository.logged_events) == 1
    assert repository.logged_events[0].step == OnboardingStep.COMPLETED
    assert result == OnboardingStep.COMPLETED


@pytest.mark.asyncio
async def test_move_to_intro_raises_when_onboarding_state_is_missing(
    fake_transaction: FakeTransaction,
) -> None:
    repository = FakeOnboardingRepository(None)

    with pytest.raises(OnboardingNotFoundError):
        await MoveOnboardingToIntroUseCase(repository, fake_transaction).execute(UserId(100))

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []


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

    with pytest.raises(OnboardingTransitionError):
        await MoveOnboardingToRulesUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.WELCOME
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []


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

    with pytest.raises(OnboardingRulesAlreadyAcceptedError):
        await AcceptOnboardingRulesUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.REGISTRATION
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []


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

    result = await CompleteOnboardingUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 0
    assert repository.logged_events == []
    assert result is None


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

    with pytest.raises(OnboardingRulesAlreadyAcceptedError):
        await AcceptOnboardingRulesUseCase(repository, fake_transaction).execute(UserId(100))

    assert state.current_step == OnboardingStep.COMPLETED
    assert state.is_complete is True
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
    assert repository.logged_events == []
