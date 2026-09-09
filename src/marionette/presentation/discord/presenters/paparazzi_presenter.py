import hikari

from marionette.domain.entities.character import CharacterGender
from marionette.presentation.discord.colors import Color


class PaparazziPresenter:
    @staticmethod
    def present(channel_id: int, character_name: str, gender: CharacterGender) -> hikari.Embed:
        return hikari.Embed(
            title="📸 Папарацци не дремлют",
            description=(
                f"Наши источники сообщают, что **{character_name}** "
                f"был{'а' if gender == CharacterGender.FEMALE else ''} замечен{'а' if gender == CharacterGender.FEMALE else ''} в <#{channel_id}>.\n\n"
                f"*Редакция продолжает следить за развитием событий.*"
            ),
            color=Color.TABLOID,
        ).set_footer(text="Эксклюзив · Токийский инсайдер")
