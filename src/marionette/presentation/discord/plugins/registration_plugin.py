from datetime import datetime

import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.usecases.register_usecase import RegisterUseCase
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.roles import Roles
from marionette.presentation.discord.helpers import UserInterfaceHelper

from marionette.domain.exceptions import CharacterBirthdayIncorrect


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
    
    try:
        birthday = datetime.strptime(
            UserInterfaceHelper.get_modal_value(raw_modal, "birthday"), "%d.%m.%Y"
        )
    except ValueError as exc:
        raise CharacterBirthdayIncorrect() from exc

    await usecase.execute(
        user_id=UserId(event.interaction.user.id),
        name=UserInterfaceHelper.get_modal_value(raw_modal, "name"),
        role=Roles(UserInterfaceHelper.get_modal_value(raw_modal, "role")),
        birthday=birthday,
        biography=UserInterfaceHelper.get_modal_value(raw_modal, "mini_bio"),
    )
