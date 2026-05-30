from importlib import resources

MAIN_TEXT = resources.files("marionette.assets.text.intro").joinpath("main.txt").read_text(encoding="utf8")
WHAT_TEXT = resources.files("marionette.assets.text.intro").joinpath("what.txt").read_text(encoding="utf8")
NEXT_TEXT = resources.files("marionette.assets.text.intro").joinpath("next.txt").read_text(encoding="utf8")
FEATURES_TEXT = resources.files("marionette.assets.text.intro").joinpath("features.txt").read_text(encoding="utf8")


class IntroPresenter:
    @staticmethod
    def present() -> str:
        return MAIN_TEXT

    @staticmethod
    def present_next() -> str:
        return NEXT_TEXT

    @staticmethod
    def present_what() -> str:
        return WHAT_TEXT

    @staticmethod
    def present_features() -> str:
        return FEATURES_TEXT
