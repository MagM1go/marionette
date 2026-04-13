from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.onboarding_base_usecase import BaseOnboardingUseCase
from marionette.domain.entities.onboarding import OnboardingStep


class StartOnboardingUseCase(BaseOnboardingUseCase):
    async def execute(self, zone_id: int, user_id: UserId) -> None:
        async with self._transaction as transaction:
            state = await self._repository.create(user_id=user_id, created_at=self._now())
            if state.current_step != OnboardingStep.NEWBIE:
                return

            await self._move(transaction, user_id, state, OnboardingStep.WELCOME)

        await self._apply_step_assets(zone_id=zone_id, user_id=user_id, step=OnboardingStep.WELCOME)
