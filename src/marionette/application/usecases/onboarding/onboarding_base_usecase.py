from datetime import UTC, datetime

from marionette.application.protocols import (
    OnboardingRepository,
    Transaction,
    UserId,
)
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState, OnboardingStep
from marionette.domain.exceptions import OnboardingNotFoundError
from marionette.domain.policies.onboarding_policy import OnboardingPolicy


class BaseOnboardingUseCase:
    def __init__(
        self,
        repository: OnboardingRepository,
        transaction: Transaction,
    ) -> None:
        self._repository = repository
        self._transaction = transaction

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    async def _get_state(self, user_id: UserId) -> OnboardingState:
        state = await self._repository.get_by_user_id(user_id)
        if state is None:
            raise OnboardingNotFoundError()

        return state

    async def _move(
        self,
        transaction: Transaction,
        user_id: UserId,
        state: OnboardingState,
        step: OnboardingStep,
    ) -> OnboardingStep:
        OnboardingPolicy.ensure_can_move(
            current=state.current_step,
            target=step,
            is_complete=state.is_complete,
        )
        state.move_to_step(step)

        await self._repository.log_event(
            OnboardingEvent(user_id=int(user_id), event_name=f"step_{step}", step=step)
        )
        await transaction.commit()
        return step
