from typing import Protocol

from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState


class OnboardingRepository(Protocol):
    async def get_by_user_id(self, user_id: int) -> OnboardingState | None: ...

    def add(self, state: OnboardingState) -> None: ...

    async def log_event(self, event: OnboardingEvent) -> None: ...
