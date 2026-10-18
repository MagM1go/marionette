import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding.reset_onboarding_usecase import OnboardingResetUseCase
from marionette.application.usecases.onboarding.start_onboarding_usecase import StartOnboardingUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.presentation.discord.presenters.welcome_presenter import WelcomePresenter
from marionette.presentation.discord.ui.onboarding.dispatcher import OnboardingActionDispatcher
from marionette.presentation.discord.ui.onboarding.registry import OnboardingAction, onboarding_registry

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
inject_plugin = inject(lambda: plugin.model.dishka())


@plugin.include
@crescent.event
@inject_plugin
async def on_user_arrive(event: hikari.MemberCreateEvent, usecase: Inject[StartOnboardingUseCase]) -> None:
    user_id = UserId(event.user_id)
    await event.app.rest.add_role_to_member(
        guild=config.discord.guild.main,
        user=event.user_id,
        role=config.discord.roles.unverified,
    )
    await usecase.execute(user_id)


@plugin.include
@crescent.event
@inject_plugin
async def on_user_leave(event: hikari.MemberDeleteEvent, usecase: Inject[OnboardingResetUseCase]) -> None:
    await usecase.reset(UserId(event.user_id))


@plugin.include
@crescent.event
@inject_plugin
async def handle_interaction_click(
    event: hikari.ComponentInteractionCreateEvent,
    dispatcher: Inject[OnboardingActionDispatcher],
) -> None:
    if event.interaction.guild_id is None:
        return

    action = onboarding_registry.get_action(event.interaction.custom_id)
    if action is None:
        return

    if action == OnboardingAction.COMPLETE:
        await event.app.rest.create_message(
            channel=config.discord.text_channels.general, content=WelcomePresenter.present_welcome(event.interaction.user.mention)
        )

    user_id = UserId(event.interaction.user.id)
    zone_id = event.interaction.guild_id

    await dispatcher.execute(action, zone_id, user_id)
