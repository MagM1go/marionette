from typing import Protocol

from marionette.application.protocols.types import RoleId, UserId
from marionette.domain.entities.onboarding import OnboardingStep


class PlayerAccessManager(Protocol):
    async def add_role(self, zone_id: int, user_id: UserId, role_id: RoleId) -> None: ...

    async def remove_role(self, zone_id: int, user_id: UserId, role_id: RoleId) -> None: ...

    async def apply_step_assets(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None: ...
