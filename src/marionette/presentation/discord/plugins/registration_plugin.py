from datetime import datetime

import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.usecases.register_usecase import RegisterUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.exceptions import CharacterBirthdayIncorrect
from marionette.domain.roles import Roles
from marionette.presentation.discord.helpers import UserInterfaceHelper
from marionette.presentation.discord.presenters.registration_presenter import RegistrationPresenter

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
        birthday = datetime.strptime(UserInterfaceHelper.get_modal_value(raw_modal, "birthday"), "%d.%m.%Y")
    except ValueError as exc:
        raise CharacterBirthdayIncorrect() from exc

    name = UserInterfaceHelper.get_modal_value(raw_modal, "name")
    role = UserInterfaceHelper.get_modal_value(raw_modal, "role")
    biography = UserInterfaceHelper.get_modal_value(raw_modal, "mini_bio")
    raw_birthday = UserInterfaceHelper.get_modal_value(raw_modal, "birthday")

    character_id = await usecase.register(
        user_id=UserId(event.interaction.user.id),
        name=name,
        role=Roles(role),
        birthday=birthday,
        biography=biography,
    )
    await plugin.app.rest.create_message(
        config.discord.moderation_channel_id,
        component=RegistrationPresenter.present_moderation(event.interaction.user.id, character_id, name, raw_birthday, role, biography),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2,
    )
