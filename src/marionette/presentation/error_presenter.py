import hikari

from marionette.presentation.colors import Color


class ErrorPresenter:
    @staticmethod
    def present(exception_message: str) -> hikari.Embed:
        return hikari.Embed(
            title="❌ Сбой!",
            description=f"Сообщение от информатора: {exception_message}",
            color=Color.ERROR
        )
