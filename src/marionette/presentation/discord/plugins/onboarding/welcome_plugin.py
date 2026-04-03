import crescent
import hikari

from marionette.application.protocols import UserId
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.entities.onboarding import OnboardingStep

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def on_user_arrive(
    event: hikari.MemberCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None:
    user_id = UserId(event.user_id)
    await usecase.move_to(event.guild_id, user_id, OnboardingStep.WELCOME)
