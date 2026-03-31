from typing import Any, Protocol

from marionette.application.protocols.types import RoleId, UserId
from marionette.domain.entities.onboarding import OnboardingStep


class PlayerAccessManager(Protocol):
    # TODO: Нормально типизировать и придумать с этим ваще чета
    role_manager: Any

    async def add_role(self, role_manager: Any, zone_id: int, user_id: UserId, role_id: RoleId) -> None: ...

    async def remove_role(self, role_manager: Any, zone_id: int, user_id: UserId, role_id: RoleId) -> None: ...

    async def apply_step_assets(
        self, role_manager: Any, zone_id: int, user_id: UserId, step: OnboardingStep
    ) -> None: ...
