from marionette.application.protocols import (
    OnboardingRepository,
    PlayerAccessManager,
    Transaction,
    UserId,
)
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingStep
from marionette.domain.exceptions import OnboardingNotFoundError


class OnboardingUseCase:
    def __init__(
        self, repository: OnboardingRepository, transaction: Transaction, access: PlayerAccessManager
    ) -> None:
        self._repository = repository
        self._transaction = transaction
        self._access = access

    async def move_to(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        async with self._transaction as transaction:
            state = await self._repository.get_by_user_id(user_id)
            if not state:
                raise OnboardingNotFoundError()

            state.current_step = step

            await self._repository.log_event(
                OnboardingEvent(user_id=int(user_id), event_name=f"step_{step}", step=step)
            )
            await transaction.commit()

        await self._access.apply_step_assets(zone_id=zone_id, user_id=user_id, step=step)
