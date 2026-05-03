from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.onboarding_base_usecase import BaseOnboardingUseCase
from marionette.domain.entities.onboarding import OnboardingStep


class MoveOnboardingToIntroUseCase(BaseOnboardingUseCase):
    async def execute(self, user_id: UserId) -> OnboardingStep | None:
        async with self._transaction as transaction:
            state = await self._get_state(user_id)
            if state.current_step >= OnboardingStep.INTRO:
                return None

            return await self._move(transaction, user_id, state, OnboardingStep.INTRO)
