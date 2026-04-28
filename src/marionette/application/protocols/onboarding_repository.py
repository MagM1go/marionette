import datetime
from typing import Protocol

from marionette.application.protocols.types import UserId
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState


class OnboardingRepository(Protocol):
    async def create(self, user_id: UserId, created_at: datetime.datetime) -> OnboardingState: ...

    async def get_by_user_id(self, user_id: UserId) -> OnboardingState | None: ...

    async def reset(self, user_id: UserId, updated_at: datetime.datetime) -> OnboardingState: ...

    async def log_event(self, event: OnboardingEvent) -> None: ...
