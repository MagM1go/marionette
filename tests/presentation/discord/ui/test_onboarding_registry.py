from marionette.presentation.discord.ui.onboarding.registry import (
    OnboardingAction,
    onboarding_registry,
)


def test_onboarding_registry_returns_screen_by_id() -> None:
    assert onboarding_registry.get_by_id("hello") is not None
    assert onboarding_registry.get_by_id("rules") is not None
    assert onboarding_registry.get_by_id("missing") is None


def test_onboarding_registry_returns_action_by_custom_id() -> None:
    assert onboarding_registry.get_action("onboarding_rules_accept_button") == OnboardingAction.ACCEPT_RULES
    assert onboarding_registry.get_action("missing") is None


def test_onboarding_registry_contains_only_persistent_views_for_interactive_screens() -> None:
    views = onboarding_registry.iter_persistent_views()

    assert len(views) == 5
    assert {type(view).__name__ for view in views} == {
        "HelloView",
        "IntroView",
        "FaqView",
        "RegistrationView",
        "RulesView",
    }
