import hikari

from marionette.application.usecases.profile.summary_usecase import SummaryData
from marionette.domain.entities.character import Character
from marionette.presentation.discord.presenters.base.embed import bot_embed


class ProfilePresenter:
    @staticmethod
    def present(issuer_id: int, icon_url: hikari.Resourceish | None, username: str, summary: SummaryData) -> hikari.Embed:
        most_chosen_role = summary.most_chosen_role or "отсутствует"

        embed = bot_embed(
            title=f"{username} // marionette",
            description=f"Подписан на **{len(summary.subscriptions)}** инфлюенсеров\n"
            + f"Любимая маска: `{most_chosen_role}`\n"
            + f"Средний возраст куколок: `{summary.average_age or 'отсутствует'}`",
            footer=hikari.EmbedFooter(text=f"Вызвал {issuer_id}", icon=icon_url),  # type: ignore
            thumbnail=hikari.EmbedImage(resource=icon_url),  # type: ignore
        )

        return embed

    @staticmethod
    def present_character_pages(summary: SummaryData) -> list[hikari.Embed]:
        return [
            hikari.Embed(
                title=f"{character.name} [{character.id}]",
                description=character.biography[:4096],
            ).add_field(
                name="Дополнительная информация",
                value=f"Дата рождения: `{character.birthday}` ({character.age})\n"
                + f"Пол персонажа: `{character.gender}`\n"
                + f"Агенство: {character.agency} ({character.agency_role})" if character.agency else "",
            ).add_field(
                name="Основная роль",
                value=character.role
            )
            for character in summary.characters
        ]

    @staticmethod
    def present_character_biography_pages(page_index: int, character: Character) -> hikari.Embed:
        return hikari.Embed(title=f"{character.name} | биография", description=character.biography[page_index * 4096 : (page_index + 1) * 4096])
