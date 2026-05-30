from importlib import resources

HOW_TO_START_TEXT = resources.files("marionette.assets.text.faq").joinpath("start.txt").read_text(encoding="utf8")
LORE_TEXT = resources.files("marionette.assets.text.faq").joinpath("lore.txt").read_text(encoding="utf8")


class FaqPresenter:
    @staticmethod
    def present() -> str:
        return "На самом деле, часто задаваемые вопросы - это лишь попытка сделать вид, что ты сближаешься с аудиторией."

    @staticmethod
    def how_to_start() -> str:
        return HOW_TO_START_TEXT

    @staticmethod
    def lore() -> str:
        return LORE_TEXT
