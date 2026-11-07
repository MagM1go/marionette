from importlib import resources

GENERAL_RULES = resources.files("marionette.assets.text.rules").joinpath("general.txt").read_text(encoding="utf8")
ROLEPLAY_RULES = resources.files("marionette.assets.text.rules.roleplay_parts")


class RulesPresenter:
    @staticmethod
    def present() -> str:
        return 'Перед общением и игрой обязательно ознакомьтесь с правилами. ' \
                'Но это, конечно, если вы не хотите вылететь сразу с "кастинга.\n"' \
                '**Нажмите на кнопку ниже для получения доступа к чатам!**'

    @staticmethod
    def general_rules() -> str:
        return GENERAL_RULES

    @staticmethod
    def roleplay_rules() -> list[str]:
        return [ROLEPLAY_RULES.joinpath(f"{part}.txt").read_text(encoding="utf8") for part in range(1, 3)]
