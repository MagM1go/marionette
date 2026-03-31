from contextlib import suppress
from typing import TypedDict

import hikari

from marionette.application.protocols import PlayerAccessManager, RoleId, UserId
from marionette.bootstrap.config import config
from marionette.domain.entities.onboarding import OnboardingStep


class StepAssets(TypedDict):
    add: tuple[RoleId, ...]
    remove: tuple[RoleId, ...]


class HikariDiscordService(PlayerAccessManager):
    async def add_role(self, rest: hikari.RESTClientImpl, guild_id: int, user_id: UserId, role_id: RoleId) -> None:
        with suppress(hikari.ForbiddenError):
            await rest.add_role_to_member(guild=guild_id, user=user_id, role=role_id)

    async def remove_role(self, rest: hikari.RESTClientImpl, guild_id: int, user_id: UserId, role_id: RoleId) -> None:
        with suppress(hikari.ForbiddenError):
            await rest.remove_role_from_member(guild=guild_id, user=user_id, role=role_id)

    async def apply_step_assets(self, rest: hikari.RESTClientImpl, guild_id: int, user_id: UserId, step: OnboardingStep) -> None:
        configs: dict[OnboardingStep, StepAssets] = {
            OnboardingStep.INTRO: {
                "add": (RoleId(config.discord.start_role_id),),
                "remove": (RoleId(config.discord.unverified_role_id),),
            },
            OnboardingStep.RULES: {
                "add": (RoleId(config.discord.unregistered_role_id),),
                "remove": (RoleId(config.discord.start_role_id),),
            },
        }

        cfg = configs.get(step)
        if cfg is None:
            return 

        for role_id in cfg["add"]:
            await self.add_role(rest, guild_id, user_id, role_id)

        for role_id in cfg["remove"]:
            await self.remove_role(rest, guild_id, user_id, role_id)
