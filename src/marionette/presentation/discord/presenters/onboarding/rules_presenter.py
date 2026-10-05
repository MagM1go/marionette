from importlib import resources

GENERAL_RULES = resources.files("marionette.assets.text.rules").joinpath("general.txt").read_text(encoding="utf8")
ROLEPLAY_RULES = resources.files("marionette.assets.text.rules").joinpath("roleplay.txt").read_text(encoding="utf8")


class RulesPresenter:
    @staticmethod
    def present() -> str:
        return "Перед общением и игрой обязательно ознакомьтесь с правилами. Но это, конечно, если вы не хотите вылететь сразу с \"кастинга\""

    @staticmethod
    def general_rules() -> str:
        return GENERAL_RULES

    @staticmethod
    def roleplay_rules() -> str:
        return ROLEPLAY_RULES
