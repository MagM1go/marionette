from marionette.domain.entities.onboarding import OnboardingStep
from marionette.domain.exceptions import OnboardingTransitionError


class OnboardingPolicy:
    @staticmethod
    def ensure_can_start(current: OnboardingStep | None, is_complete: bool) -> None:
        if is_complete:
            raise OnboardingTransitionError("Onboarding already completed")
            
        if current is not None:
            raise OnboardingTransitionError("Onboarding already started")

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

        if current != OnboardingStep.REGISTRATION:
            raise OnboardingTransitionError(f"Cannot complete onboarding from step {current}")
