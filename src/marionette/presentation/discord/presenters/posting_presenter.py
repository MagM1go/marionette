from pathlib import Path

import hikari


class PostingPresenter:
    SEPARATOR_DELIMITER = "---"
    LOGOS_PATH = Path("src/marionette/presentation/assets/logos")

    @staticmethod
    def present(
        username: str, author_id: int, source: str, image: str | None, message: str
    ) -> list[hikari.api.ComponentBuilder]:
        components = PostingPresenter._build_message_components(message)

        if image:
            components.append(PostingPresenter._build_media_image(image))

        components.append(PostingPresenter._build_author_info(username, author_id, source))

        return components

    @staticmethod
    def _build_message_components(message: str) -> list[hikari.api.ComponentBuilder]:
        message_parts = message.split(PostingPresenter.SEPARATOR_DELIMITER)
        components: list[hikari.api.ComponentBuilder] = []

        for index, part in enumerate(message_parts):
            components.append(hikari.impl.TextDisplayComponentBuilder(content=part.strip()))

            if index < len(message_parts) - 1:
                components.append(
                    hikari.impl.SeparatorComponentBuilder(
                        spacing=hikari.SpacingType.SMALL, divider=True
                    )
                )

        return components

    @staticmethod
    def _build_media_image(image: hikari.Resourceish) -> hikari.api.ComponentBuilder:
        return hikari.impl.MediaGalleryComponentBuilder(
            items=[hikari.impl.MediaGalleryItemBuilder(media=image)]
        )

    @staticmethod
    def _build_author_info(
        username: str, author_id: int, source: str
    ) -> hikari.api.ComponentBuilder:
        return hikari.impl.TextDisplayComponentBuilder(
            content=f"-# @{username} | {author_id} // {source}"
        )
