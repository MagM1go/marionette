from datetime import UTC, datetime

import hikari

_EMBED_COLOR: int = 0x3E2E92


# Proxy method for embed creation
def bot_embed(
    title: str | None = None,
    description: str | None = None,
    image: hikari.EmbedImage | None = None,
    thumbnail: hikari.EmbedImage | None = None,
    *,
    footer: hikari.EmbedFooter,
) -> hikari.Embed:
    return (
        hikari.Embed(title=title, description=description, color=_EMBED_COLOR, timestamp=datetime.now(UTC))
        .set_footer(text=footer.text, icon=footer.icon)

        .set_thumbnail(thumbnail)
    )
