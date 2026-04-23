from datetime import date

import hikari


def age_from_birthday(birthday: str) -> int:
    today = date.today()
    born = date.strptime(birthday, "%d.%m.%Y")
    return date.today().year - born.year - ((today.month, today.day) < (born.month, born.day))


class RegistrationPresenter:
    @staticmethod
    def present() -> str:
        return "Верно, самое время создать своё альтер-эго для этого мира?"

    # TODO: добавить экранирование markdown'a
    #   добавить возможность добавления изображения персонажа
    @staticmethod
    def present_moderation(
        name: str, birthday: str, role: str, biography: str
    ) -> hikari.api.ComponentBuilder:
        return (
            hikari.impl.ContainerComponentBuilder()
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
        return "Персонаж был отправлен на модерацию! Ожидайте решения. В случае успешного принятия, вы будете уведомлены, а в Вашем профиле появится персонаж"
