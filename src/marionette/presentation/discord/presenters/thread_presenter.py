import hikari


class ThreadPresenter:
    @staticmethod
    def success() -> str:
        return "Ветка успешно создана"

    @staticmethod
    def present(name: str, description: str) -> hikari.impl.ContainerComponentBuilder:
        return (
            hikari.impl.ContainerComponentBuilder()
            .add_text_display(content=f"# > {name}")
            .add_text_display(content=description)
            .add_text_display(content="-# Будь осторожен.")
        )
