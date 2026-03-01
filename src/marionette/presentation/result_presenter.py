import hikari

from marionette.application.dto.embed import Embed
from marionette.application.dto.result import Result
from marionette.presentation.colors import Color


class ResultPresenter:
    @staticmethod
    def present(result: Result) -> str | hikari.Embed | tuple[str, hikari.Embed]:
        hikari_embed = (
            ResultPresenter._to_hikari_embed(result.embed) if result.embed else None
        )
    
        match (result.content, hikari_embed):
            case (str(content), None):
                return content
            case (None, hikari.Embed() as embed):
                return embed
            case (str(content), hikari.Embed() as embed):
                return content, embed
            case _:
                raise ValueError("Result должен быть не пустым")

    @staticmethod
    def _to_hikari_embed(embed: Embed) -> hikari.Embed:
        hikari_embed = hikari.Embed(color=embed.color or Color.DEFAULT)
        
        if embed.title:
            hikari_embed.title = embed.title
            
        if embed.description:
            hikari_embed.description = embed.description
            
        if embed.url:
            hikari_embed.url = embed.url

        if embed.thumbnail_url:
            hikari_embed.set_thumbnail(embed.thumbnail_url)

        if embed.image_url:
            hikari_embed.set_image(embed.image_url)

        if embed.footer:
            hikari_embed.set_footer(embed.footer)

        return hikari_embed
