import pytest

from marionette.application.protocols import RoleId, UserId
from marionette.bootstrap.config import config
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.ui.onboarding.step_assets import OnboardingStepAssets


class FakeRest:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int, UserId, RoleId]] = []

    async def add_role_to_member(self, guild: int, user: UserId, role: RoleId) -> None:
        self.calls.append(("add", guild, user, role))

    async def remove_role_from_member(self, guild: int, user: UserId, role: RoleId) -> None:
        self.calls.append(("remove", guild, user, role))


@pytest.mark.asyncio
async def test_onboarding_step_assets_applies_intro_roles() -> None:
    rest = FakeRest()
    step_assets = OnboardingStepAssets(rest)  # type: ignore[arg-type]

    await step_assets.apply(zone_id=777, user_id=UserId(100), step=OnboardingStep.INTRO)

    assert rest.calls == [
        ("add", 777, UserId(100), RoleId(config.discord.start_role_id)),
        ("remove", 777, UserId(100), RoleId(config.discord.unverified_role_id)),
    ]


@pytest.mark.asyncio
async def test_onboarding_step_assets_ignores_steps_without_discord_assets() -> None:
    rest = FakeRest()
    step_assets = OnboardingStepAssets(rest)  # type: ignore[arg-type]

    await step_assets.apply(zone_id=777, user_id=UserId(100), step=OnboardingStep.COMPLETED)

    assert rest.calls == []
