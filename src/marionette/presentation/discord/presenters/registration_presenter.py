from datetime import date

import hikari

from hikari.impl import ContainerComponentBuilder
from hikari.impl import TextDisplayComponentBuilder
from marionette.application.protocols.types import CharacterId


def age_from_birthday(birthday: str) -> int:
    today = date.today()
    born = date.strptime(birthday, "%d.%m.%Y")
    return date.today().year - born.year - ((today.month, today.day) < (born.month, born.day))


class RegistrationPresenter:
    @staticmethod
    def present() -> str:
        return "Время создавать своё альтер-эго."

    @staticmethod
    def present_moderation(
        user_id: int, user_mention: str, character_id: CharacterId, name: str, birthday: str, role: str, biography: str
    ) -> list[TextDisplayComponentBuilder | ContainerComponentBuilder]:
        return [
            hikari.impl.TextDisplayComponentBuilder(content=user_mention),
            (hikari.impl.ContainerComponentBuilder()
            .add_text_display(f"Персонаж <@{user_id}> ({user_id}); ID: {character_id}")
            .add_text_display(f"Имя персонажа: `{name}`")
            .add_text_display(
                f"День рождения персонажа: `{birthday}`, возраст: `{age_from_birthday(birthday)}`"
            )
            .add_text_display(f"Роль: {role}")
            )
        ]

    @staticmethod
    def present_user() -> str:
        return "Персонаж был отправлен на модерацию! Ожидайте решения. В случае успешного принятия, вы будете уведомлены, а в профиле появится персонаж."
