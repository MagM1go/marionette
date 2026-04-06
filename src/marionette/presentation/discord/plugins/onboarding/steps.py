import typing as t

from marionette.domain.entities.onboarding import OnboardingStep

ONBOARDING_HELLO_CUSTOM_ID: t.Final[str] = "onboarding_hello_button"
ONBOARDING_INTRO_CUSTOM_ID: t.Final[str] = "onboarding_welcome_button"

# Указывает, какой шаг будет следующим после нажатия кнопки с айди из ключа
ID_TO_STEP: t.Final[dict[str, OnboardingStep]] = {
    ONBOARDING_HELLO_CUSTOM_ID: OnboardingStep.INTRO,
    ONBOARDING_INTRO_CUSTOM_ID: OnboardingStep.RULES,
}
