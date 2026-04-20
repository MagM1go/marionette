from importlib import resources

HELLO_TEXT = resources.files("marionette.assets.text").joinpath("hello.txt").read_text(encoding="utf8")


class HelloPresenter:
    @staticmethod
    def present() -> str:
        return HELLO_TEXT
