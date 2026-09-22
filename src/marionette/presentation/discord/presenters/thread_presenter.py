import hikari


class ThreadPresenter:
    @staticmethod
    def success() -> str:
        return "Ветка успешно создана"

    @staticmethod
    def present(name: str, description: str) -> hikari.impl.TextDisplayComponentBuilder:
        return hikari.impl.TextDisplayComponentBuilder(content=f"# {name}\n```{description}```")
