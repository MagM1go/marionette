from datetime import UTC, datetime

from marionette.application.policy.onboarding_policy import OnboardingPolicy
from marionette.application.protocols import IOnboardingRepository, UserId
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.domain.exceptions import OnboardingTransitionError


class OnboardingUseCase:
    def __init__(self, repository: IOnboardingRepository) -> None:
        self._repository = repository

    async def start(self, user_id: UserId) -> None:
        self._repository.start(user_id)
        await self._repository.log_event(
            user_id=user_id,
            event_name="started",
            created_at=datetime.now(UTC),
        )

    async def _get_current_step(self, user_id: UserId) -> OnboardingStep:
        current_step = await self._repository.get_current_step(user_id)

        if current_step is None:
            raise OnboardingTransitionError(f"Onboarding was not started for user {user_id}")

        return current_step

    async def set_next_step(self, user_id: UserId, step: OnboardingStep) -> None:
        current = await self._get_current_step(user_id)
        is_complete = await self._repository.is_complete(user_id)

        OnboardingPolicy.ensure_can_move(current, step, is_complete)

        await self._repository.set_current_step(user_id, step)
        await self._repository.log_event(
            user_id=user_id,
            event_name="next_step",
            step=step,
            created_at=datetime.now(UTC),
            metadata={"from": str(current), "to": str(step)},
        )

    async def complete(self, user_id: UserId) -> None:
        current = await self._get_current_step(user_id)
        is_complete = await self._repository.is_complete(user_id)

        OnboardingPolicy.ensure_can_complete(current, is_complete)

        await self._repository.set_complete(user_id)
        await self._repository.log_event(
            user_id=user_id,
            event_name="complete",
            step=current,
            created_at=datetime.now(UTC),
        )
