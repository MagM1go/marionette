from datetime import datetime
from typing import cast

import aiohttp
import crescent
import hikari

from marionette.application.protocols.types import UserId
from marionette.application.usecases.character.register_character_usecase import RegisterUseCase
from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.bootstrap.di.inject import Inject, inject
from marionette.domain.entities.character import CharacterGender
from marionette.domain.exceptions import CharacterBirthdayIncorrect
from marionette.domain.roles import Roles
from marionette.presentation.discord.helpers import UserInterfaceHelper
from marionette.presentation.discord.presenters.registration_presenter import RegistrationPresenter

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()
http_session = aiohttp.ClientSession()


async def is_image(url: str | None) -> bool:
    if url is None:
        return False
        
    async with http_session.get(url) as response:
        return "image" in response.content_type


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
        birthday = datetime.strptime(cast(str, UserInterfaceHelper.get_modal_value(raw_modal, "birthday")), "%d.%m.%Y")
    except ValueError as exc:
        raise CharacterBirthdayIncorrect() from exc

    name = UserInterfaceHelper.get_modal_value(raw_modal, "name")
    assert name is not None

    role = UserInterfaceHelper.get_modal_value(raw_modal, "role")
    assert role is not None

    raw_birthday = UserInterfaceHelper.get_modal_value(raw_modal, "birthday")
    assert raw_birthday is not None

    gender = UserInterfaceHelper.get_modal_value(raw_modal, "gender")
    assert gender is not None

    image_url = UserInterfaceHelper.get_modal_value(raw_modal, "image_url")

    character_id = await usecase.register(
        user_id=UserId(event.interaction.user.id),
        name=name,
        role=Roles(role),
        birthday=birthday,
        gender=CharacterGender(gender),
        image_url=image_url,
    )

    await plugin.app.rest.create_forum_post(
        config.discord.forum_channels.character,
        name,
        components=RegistrationPresenter.present_moderation(
            user_id=event.interaction.user.id,
            user_mention=event.interaction.user.mention,
            character_id=character_id,
            name=name,
            birthday=raw_birthday,
            role=Roles(role),
            image_url=image_url,
        ),
        flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        user_mentions=True,
        attachment=image_url if image_url and await is_image(image_url) else hikari.UNDEFINED,
    )


@plugin.include
@crescent.event
async def on_shutdown(_: hikari.events.StoppingEvent) -> None:
    await http_session.close()
