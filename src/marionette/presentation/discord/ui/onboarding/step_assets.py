from contextlib import suppress
from typing import TypedDict

import hikari

from marionette.application.protocols import RoleId, UserId
from marionette.bootstrap.config import config
from marionette.domain.entities.onboarding import OnboardingStep


class StepAssets(TypedDict):
    add: tuple[RoleId, ...]
    remove: tuple[RoleId, ...]


class OnboardingStepAssets:
    def __init__(self, rest: hikari.api.RESTClient) -> None:
        self._rest = rest

    async def add_role(self, zone_id: int, user_id: UserId, role_id: RoleId) -> None:
        with suppress(hikari.ForbiddenError):
            await self._rest.add_role_to_member(guild=zone_id, user=user_id, role=role_id)

    async def remove_role(self, zone_id: int, user_id: UserId, role_id: RoleId) -> None:
        with suppress(hikari.ForbiddenError):
            await self._rest.remove_role_from_member(guild=zone_id, user=user_id, role=role_id)

    async def apply(self, zone_id: int, user_id: UserId, step: OnboardingStep) -> None:
        configs: dict[OnboardingStep, StepAssets] = {
            OnboardingStep.INTRO: {
                "add": (RoleId(config.discord.start_role_id),),
                "remove": (RoleId(config.discord.unverified_role_id),),
            },
            OnboardingStep.RULES: {
                "add": (RoleId(config.discord.unregistered_role_id),),
                "remove": (RoleId(config.discord.start_role_id),),
            },
            OnboardingStep.REGISTRATION: {
                "add": (RoleId(config.discord.text_role_id),),
                "remove": (),
            },
        }

        assets = configs.get(step)
        if assets is None:
            return

        for role_id in assets["add"]:
            await self.add_role(zone_id, user_id, role_id)

        for role_id in assets["remove"]:
            await self.remove_role(zone_id, user_id, role_id)
