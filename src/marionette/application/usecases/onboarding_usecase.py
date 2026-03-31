from typing import Any

from marionette.application.protocols import (
    OnboardingRepository,
    PlayerAccessManager,
    UnitOfWork,
    UserId,
)
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingStep
from marionette.domain.exceptions import OnboardingNotFoundError


class OnboardingUseCase:
    def __init__(
        self, repository: OnboardingRepository, uow: UnitOfWork, access: PlayerAccessManager
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._access = access

    # role_manager здесь просто заглушка на время, со следующим патчем это будет переделано
    async def move_to(self, role_manager: Any, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        async with self._uow as uow:
            state = await self._repository.get_by_user_id(user_id)
            if not state:
                raise OnboardingNotFoundError()

            state.current_step = step

            await self._repository.log_event(
                OnboardingEvent(user_id=int(user_id), event_name=f"step_{step}", step=step)
            )
            await uow.commit()

        await self._access.apply_step_assets(role_manager, zone_id=zone_id, user_id=user_id, step=step)
