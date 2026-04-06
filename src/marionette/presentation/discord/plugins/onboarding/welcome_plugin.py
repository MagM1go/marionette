import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.presentation.discord.plugins.onboarding.steps import ID_TO_STEP

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@plugin.include
@crescent.event
@inject_plugin
async def on_user_arrive(
    event: hikari.MemberCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None:
    user_id = UserId(event.user_id)
    await usecase.move_to(event.guild_id, user_id, OnboardingStep.WELCOME)


@plugin.include
@crescent.event
@inject_plugin
async def on_interaction_click(
    event: hikari.ComponentInteractionCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None:
    if event.interaction.guild_id is None:
        return

    if (custom_id := event.interaction.custom_id) not in ID_TO_STEP:
        return

    await usecase.move_to(
        event.interaction.guild_id, UserId(event.interaction.user.id), ID_TO_STEP[custom_id]
    )
