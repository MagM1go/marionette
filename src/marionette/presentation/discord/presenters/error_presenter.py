from datetime import UTC, datetime

import hikari

from marionette.domain import exceptions as exc
from marionette.presentation.discord import exceptions as dis_exc
from marionette.presentation.discord.colors import Color

_MESSAGES: dict[type, str] = {
    exc.CharacterNotInLocation: "Персонаж нигде не активен! Увы...",
    exc.CharacterWithoutAgencyError: "У персонажа нет агенства, не удалось убрать рейтинг.",
    exc.CharacterBirthdayIncorrect: "Убедитесь, что вы правильно ввели дату рождения персонажа. Формат: `дд-мм-гггг`",
    exc.TooManyCharacters: "Кажется, у вас слишком много персонажей. Увы, но более трёх создать нельзя.",
    exc.OnboardingRulesAlreadyAcceptedError: "Вы уже приняли правила. Повторно нажимать на кнопку не нужно.",
    exc.CharacterIsAbandoned: "Персонаж был исключён из системы. Увы, но это действие выполнить над ним нельзя",
    exc.CharacterAlreadyActive: "Персонаж активен и подобное действие в его состоянии выполнить нельзя",
    dis_exc.DmsNotAllowed: "Команду нельзя использовать в личных сообщениях.",
    dis_exc.InsufficientPermissions: "У вас недостаточно прав на исполнение. Впрочём, как и обычно.",
    dis_exc.MemberNotFound: "Участник не был найден. Или вышел, или указан не тот.",
}


class ErrorPresenter:
    @staticmethod
    def present(e: Exception) -> hikari.Embed:
        match e:
            case exc.CharacterNotFound(name=name):
                text = f"Персонаж **{name}** не найден!"
            case exc.CharacterNotActive(name=name):
                text = f"Персонаж **{name}** пока не может быть использован. Статус персонажа можно узнать в профиле."
            case exc.AlreadyInLocation(channel_id=cid):
                text = f"Персонаж уже активен в <#{cid}>! Воспользуйтесь `/exit`"
            case exc.AnotherCharacterIsActive(character_name=name):
                text = f"У вас уже есть активный персонаж! Вы забыли про **{name}**?"
            case exc.WrongChannel(expected_channel_id=cid):
                text = f"Выйти можно только из канала <#{cid}>!"
            case exc.VoteOnCooldown(character_name=name, remaining_time=time):
                text = (
                    f"За **{name}** уже недавно голосовали. "
                    f"Следующий голос доступен в **{(datetime.now(UTC) + time).strftime('%d.%m, %H:%M:%S')}** "
                    "(часовой пояс бота: +3 от Москвы)"
                )
            case _:
                text = _MESSAGES.get(type(e), "Произошла неизвестная ошибка.")

        return hikari.Embed(
            title="❌ Сбой!",
            description=f"Сообщение от информатора: {text}",
            color=Color.ERROR,
        )
