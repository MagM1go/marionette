import hikari

from marionette.domain import exceptions as exc
from marionette.presentation.discord import exceptions as dis_exc
from marionette.presentation.discord.colors import Color

_MESSAGES: dict[type, str] = {
    exc.CharacterNotInLocation: "Персонаж нигде не активен! Увы...",
    exc.CharacterWithoutAgencyError: "У персонажа нет агенства, не удалось убрать рейтинг.",
    exc.OnboardingRulesAlreadyAcceptedError: "Вы уже приняли правила. Повторно нажимать на кнопку не нужно.",
    dis_exc.DmsNotAllowed: "Команду нельзя использовать в личных сообщениях."
}


class ErrorPresenter:
    @staticmethod
    def present(e: Exception) -> hikari.Embed:
        match e:
            case exc.CharacterNotFound(name=name):
                text = f"У вас нет персонажа с именем **{name}**!"
            case exc.AlreadyInLocation(channel_id=cid):
                text = f"Персонаж уже активен в <#{cid}>! Воспользуйтесь `/exit`"
            case exc.AnotherCharacterIsActive(character_name=name):
                text = f"У вас уже есть активный персонаж! Вы забыли про **{name}**?"
            case exc.WrongChannel(expected_channel_id=cid):
                text = f"Выйти можно только из канала <#{cid}>!"
            case _:
                text = _MESSAGES.get(type(e), "Произошла неизвестная ошибка.")

        return hikari.Embed(
            title="❌ Сбой!",
            description=f"Сообщение от информатора: {text}",
            color=Color.ERROR,
        )
