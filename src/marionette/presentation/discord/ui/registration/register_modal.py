import typing as t
from datetime import date

import hikari
import miru

from marionette.bootstrap.config import config
from marionette.domain.exceptions import CharacterIsTooYoung
from marionette.domain.roles import Roles
from marionette.presentation.discord.presenters.registration_presenter import (
    RegistrationPresenter,
    age_from_birthday,
)
from marionette.presentation.discord.ui.wrapper.modal_v2 import ModalV2
from marionette.presentation.discord.ui.wrapper.string_select_menu import StringSelect


class RegistrationModal(ModalV2):
    def __init__(self) -> None:
        super().__init__("Регистрация", custom_id="registration_window", timeout=None)

    name = miru.TextInput(
        custom_id="name",
        label="Имя или псевдоним персонажа",
        required=True,
        placeholder="Серафим / Анна Браун / Фантом",
    )
    birthday = miru.TextInput(
        custom_id="birthday",
        label="День рождения персонажа (дд.мм.гггг)",
        required=True,
        placeholder="31.10.2010",
    )
    mini_bio = miru.TextInput(
        custom_id="mini_bio",
        label="Биография (коротко, мин. 200 символов)",
        required=True,
        min_length=200,
        style=hikari.TextInputStyle.PARAGRAPH,
    )
    role = StringSelect(
        custom_id="role",
        label="Роль в шоу",
        options=[miru.SelectOption(label=r, value=r) for r in Roles],
    )

    async def modal_check(self, context: miru.ModalContext) -> bool:
        birthday = context.values[self.birthday]

        try:
            date.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    async def callback(self, context: miru.ModalContext) -> None:
        name = t.cast(str, self.name.value)
        birthday = t.cast(str, self.birthday.value)
        bio = t.cast(str, self.mini_bio.value)
        role = t.cast(str, self.role.value)

        if age_from_birthday(birthday) < 13:
            raise CharacterIsTooYoung()

        await context.respond(
            RegistrationPresenter.present_user(), flags=hikari.MessageFlag.EPHEMERAL
        )
        await context.client.rest.create_message(
            config.discord.moderation_channel_id,
            component=RegistrationPresenter.present_moderation(name, birthday, role, bio),
            flags=hikari.MessageFlag.IS_COMPONENTS_V2,
        )
