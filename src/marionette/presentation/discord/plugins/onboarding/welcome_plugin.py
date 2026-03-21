import crescent
import hikari

from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.presentation.di.container import CrescentContainer
from marionette.presentation.di.inject import Inject, inject

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def on_user_arrive(
    event: hikari.MemberCreateEvent, usecase: Inject[OnboardingUseCase]
) -> None: ...
