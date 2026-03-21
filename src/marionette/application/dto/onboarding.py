from dataclasses import dataclass, field

from marionette.domain.entities.onboarding import OnboardingStep


@dataclass(slots=True)
class OnboardingAction:
    step: OnboardingStep
    roles_to_add: list[int] = field(default_factory=list)
    roles_to_remove: list[int] = field(default_factory=list)
    message: str | None = None
    complete: bool = False
