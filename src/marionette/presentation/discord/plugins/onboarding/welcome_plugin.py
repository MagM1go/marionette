import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding_reset_usecase import OnboardingResetUseCase
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.ui.onboarding import onboarding_registry

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@plugin.include
@crescent.event
@inject_plugin
async def on_user_arrive(
    event: hikari.MemberCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None:
    user_id = UserId(event.user_id)
    await event.app.rest.add_role_to_member(
        guild=config.discord.main_guild_id,
        user=event.user_id,
        role=config.discord.unverified_role_id,
    )
    await usecase.start(event.guild_id, user_id)


@plugin.include
@crescent.event
@inject_plugin
async def on_user_leave(
    event: hikari.MemberDeleteEvent, usecase: Inject[OnboardingResetUseCase]
) -> None:
    await usecase.reset(UserId(event.user_id))


@plugin.include
@crescent.event
@inject_plugin
async def on_interaction_click(
    event: hikari.ComponentInteractionCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None:
    if event.interaction.guild_id is None:
        return

    step = onboarding_registry.get_target_step(event.interaction.custom_id)
    if step is None:
        return

    await usecase.move_to(
        event.interaction.guild_id,
        UserId(event.interaction.user.id),
        step,
    )
