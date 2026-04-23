from datetime import datetime

import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.usecases.register_usecase import RegisterUseCase
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.roles import Roles
from marionette.presentation.discord.helpers import UserInterfaceHelper


plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.event
@inject(lambda: plugin.model.dishka())
async def on_register_modal_submit(
    event: hikari.ModalInteractionCreateEvent,
    usecase: Inject[RegisterUseCase],
) -> None:
    if event.interaction.custom_id != "registration_window":
        return

    raw_modal = UserInterfaceHelper.labeled_modal_map(event.interaction.components)
    await usecase.execute(
        user_id=UserId(event.interaction.user.id),
        name=UserInterfaceHelper.get_modal_value(raw_modal, "name"),
        role=Roles(UserInterfaceHelper.get_modal_value(raw_modal, "role")),
        birthday=datetime.strptime(
            UserInterfaceHelper.get_modal_value(raw_modal, "birthday"), "%d.%m.%Y"
        ),
        biography=UserInterfaceHelper.get_modal_value(raw_modal, "mini_bio"),
    )
