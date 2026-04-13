from datetime import UTC, datetime

from marionette.application.protocols import (
    OnboardingRepository,
    PlayerAccessManager,
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
        access: PlayerAccessManager,
    ) -> None:
        self._repository = repository
        self._transaction = transaction
        self._access = access

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
    ) -> None:
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

    async def _apply_step_assets(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        await self._access.apply_step_assets(zone_id=zone_id, user_id=user_id, step=step)
