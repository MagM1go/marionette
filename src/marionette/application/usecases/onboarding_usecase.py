from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from marionette.application.protocols import IOnboardingRepository, UserId
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.domain.exceptions import OnboardingTransitionError
from marionette.domain.policies.onboarding_policy import OnboardingPolicy


class OnboardingUseCase:
    def __init__(self, repository: IOnboardingRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UserId, step: OnboardingStep) -> None:
        handlers: dict[OnboardingStep, Callable[[UserId], Any]] = {
            OnboardingStep.WELCOME: self.hello_step,
            OnboardingStep.INTRO: self.introduction_step,
            OnboardingStep.RULES: self.rule_step,
            OnboardingStep.DRAFT_REGISTRATION: self.draft_registration_step,
            OnboardingStep.FULL_REGISTRATION: self.full_registration_step,
        }

        handler = handlers.get(step)
        if handler:
            await handler(user_id)

    async def start(self, user_id: UserId) -> None:
        current = await self._repository.get_current_step(user_id)
        is_complete = await self._repository.is_complete(user_id)

        OnboardingPolicy.ensure_can_start(current, is_complete)

        self._repository.start(user_id)
        await self._repository.log_event(
            user_id=user_id,
            event_name="started",
            created_at=datetime.now(UTC),
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

    async def _get_current_step(self, user_id: UserId) -> OnboardingStep:
        current_step = await self._repository.get_current_step(user_id)
        if current_step is None:
            raise OnboardingTransitionError(f"Onboarding was not started for user {user_id}")

        return current_step

    async def _set_next_step(self, user_id: UserId, step: OnboardingStep) -> None:
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

    # я не уверен в эти прокси методах, возможно часть уберу, но мб в каких-то всё же появится своя логика.
    async def hello_step(self, user_id: UserId) -> None:
        await self._set_next_step(user_id, OnboardingStep.WELCOME)

    async def introduction_step(self, user_id: UserId) -> None:
        await self._set_next_step(user_id, OnboardingStep.INTRO)

    async def rule_step(self, user_id: UserId) -> None:
        await self._set_next_step(user_id, OnboardingStep.RULES)

    async def draft_registration_step(self, user_id: UserId) -> None:
        await self._set_next_step(user_id, OnboardingStep.DRAFT_REGISTRATION)

    async def full_registration_step(self, user_id: UserId) -> None:
        await self._set_next_step(user_id, OnboardingStep.FULL_REGISTRATION)
