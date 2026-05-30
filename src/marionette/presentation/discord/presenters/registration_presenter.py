from datetime import date

import hikari

from marionette.application.protocols.types import CharacterId


def age_from_birthday(birthday: str) -> int:
    today = date.today()
    born = date.strptime(birthday, "%d.%m.%Y")
    return date.today().year - born.year - ((today.month, today.day) < (born.month, born.day))


class RegistrationPresenter:
    @staticmethod
    def present() -> str:
        return "Cамое время создать своё альтер-эго, верно?"

    # TODO: добавить экранирование markdown'a
    #   добавить возможность добавления изображения персонажа
    @staticmethod
    def present_moderation(
        user_id: int, character_id: CharacterId, name: str, birthday: str, role: str, biography: str
    ) -> hikari.api.ComponentBuilder:
        return (
            hikari.impl.ContainerComponentBuilder()
            .add_text_display(f"ПЕРСОНАЖ ОТ <@{user_id}> ({user_id}); ID: {character_id}")
            .add_text_display(f"Имя персонажа: `{name}`")
            .add_text_display(
                f"День рождения персонажа: `{birthday}`, возраст: `{age_from_birthday(birthday)}`"
            )
            .add_text_display(f"Роль: {role}")
            .add_separator()
            .add_text_display(biography)
        )

    @staticmethod
    def present_user() -> str:
        return "Персонаж был отправлен на модерацию! Ожидайте решения. В случае успешного принятия, вы будете уведомлены, а в профиле появится персонаж"
