from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.ui.onboarding import onboarding_registry


def test_onboarding_registry_maps_custom_ids_to_steps() -> None:
    assert onboarding_registry.get_target_step("onboarding_hello_button") == OnboardingStep.INTRO
    assert onboarding_registry.get_target_step("onboarding_intro_button_next") == OnboardingStep.RULES
    assert onboarding_registry.get_target_step("onboarding_intro_button_about") is None


def test_onboarding_registry_contains_only_persistent_views_for_interactive_screens() -> None:
    views = onboarding_registry.iter_persistent_views()

    assert len(views) == 4
    assert {type(view).__name__ for view in views} == {"HelloView", "IntroView", "FaqView", "RulesView"}
