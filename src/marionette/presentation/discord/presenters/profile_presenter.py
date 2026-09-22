from collections.abc import Sequence

import hikari

from marionette.application.usecases.profile.summary_usecase import SummaryData
from marionette.domain.entities.character import Character
from marionette.presentation.discord.presenters.base.embed import bot_embed


class ProfilePresenter:
    @staticmethod
    def present(
        issuer_id: int, issuer_icon_url: hikari.Resourceish | None, icon_url: hikari.Resourceish | None, username: str, summary: SummaryData
    ) -> hikari.Embed:
        most_chosen_role = summary.most_chosen_role or "отсутствует"

        embed = bot_embed(
            title=f"{username} // marionette",
            description=f"Подписан на **{len(summary.subscriptions)}** инфлюенсеров\n"
            + f"Любимая маска: `{most_chosen_role}`\n"
            + f"Средний возраст куколок: `{summary.average_age or 'отсутствует'}`",
            footer=hikari.EmbedFooter(text=f"Вызвал {issuer_id}", icon=issuer_icon_url),  # type: ignore
            thumbnail=hikari.EmbedImage(resource=icon_url),  # type: ignore
        )

        return embed

    @staticmethod
    def present_character_pages(characters: Sequence[Character]) -> list[hikari.Embed]:
        return [
            hikari.Embed(title=f"{character.name} [{character.id}]")
            .add_field(
                name="Досье",
                value=f"Дата рождения: <t:{int(character.birthday.timestamp())}:D> ({character.age})\n"
                + f"Пол персонажа: **{character.gender}**\n"
                + f"Репутация: **{character.rating}**\n"
                + (f"Агенство: {character.agency} ({character.agency_role})" if character.agency else ""),
                inline=True,
            )
            .add_field(name="Основная роль", value=character.role, inline=True)
            for character in characters
        ]

    @staticmethod
    def present_character_biography_pages(character: Character) -> list[hikari.Embed]:
        return [
            hikari.Embed(title=f"{character.name} | биография", description=character.biography[i * 4096 : (i + 1) * 4096])
            for i in range(len(character.biography) // 4096 + 1)
        ]
