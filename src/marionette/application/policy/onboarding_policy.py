from marionette.application.usecases.onboarding_usecase import OnboardingTransitionError
from marionette.domain.entities.onboarding import OnboardingStep


class OnboardingPolicy:
    @staticmethod
    def ensure_can_move(current: OnboardingStep, target: OnboardingStep, is_complete: bool) -> None:
        if is_complete:
            raise OnboardingTransitionError("Onboarding already completed")

        if target != current + 1:
            raise OnboardingTransitionError(f"Invalid onboarding transition: {current} -> {target}")

    @staticmethod
    def ensure_can_complete(
        current: OnboardingStep,
        is_complete: bool,
    ) -> None:
        if is_complete:
            raise OnboardingTransitionError("Onboarding already completed")

        if current != OnboardingStep.FULL_REGISTRATION:
            raise OnboardingTransitionError(f"Cannot complete onboarding from step {current}")
