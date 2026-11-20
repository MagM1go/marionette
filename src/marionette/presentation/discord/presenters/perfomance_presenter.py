import hikari


class PerfomancePresenter:
    @staticmethod
    def present(title: str, url: str, description: str, character_id: int, perfomance_id: int) -> list[hikari.api.ComponentBuilder]:
        return [
            hikari.impl.TextDisplayComponentBuilder(content=f"# [{title}]({url})\n{description}"),
            hikari.impl.SeparatorComponentBuilder(),
            hikari.impl.TextDisplayComponentBuilder(content=f"-# Идентификатор персонажа: **{character_id}**"),
            hikari.impl.MessageActionRowBuilder(
                components=[
                    hikari.impl.InteractiveButtonBuilder(emoji="👍", style=hikari.ButtonStyle.PRIMARY, custom_id=f"like_{perfomance_id}"),
                    hikari.impl.InteractiveButtonBuilder(emoji="👌", style=hikari.ButtonStyle.PRIMARY, custom_id=f"ok_{perfomance_id}"),
                    hikari.impl.InteractiveButtonBuilder(emoji="👎", style=hikari.ButtonStyle.PRIMARY, custom_id=f"dislike_{perfomance_id}"),
                ]
            ),
        ]
