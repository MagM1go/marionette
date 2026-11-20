import hikari


class PerfomancePresenter:
    @staticmethod
    def present(title: str, url: str, description: str, character_id: int) -> hikari.api.ContainerComponentBuilder:
        return hikari.impl.ContainerComponentBuilder(
            components=[
                hikari.impl.TextDisplayComponentBuilder(content=f"# [{title}]({url})\n{description}"),
                hikari.impl.SeparatorComponentBuilder(),
                hikari.impl.TextDisplayComponentBuilder(content=f"-# Идентификатор персонажа: **{character_id}**"),
            ]
        )
