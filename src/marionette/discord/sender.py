import crescent
import hikari


async def send_result(
    rest: hikari.api.RESTClient,
    channel_id: int,
    response: str | hikari.Embed | tuple[str, hikari.Embed],
) -> None:
    if isinstance(response, str):
        await rest.create_message(channel_id, response)
    elif isinstance(response, hikari.Embed):
        await rest.create_message(channel_id, embed=response)
    else:
        content, embed = response
        await rest.create_message(channel_id, content, embed=embed)


async def send_result_with_context(
    context: crescent.Context,
    response: str | hikari.Embed | tuple[str, hikari.Embed],
    ephemeral: bool = False
) -> None:
    if isinstance(response, str):
        await context.respond(response, ephemeral=ephemeral)
    elif isinstance(response, hikari.Embed):
        await context.respond(embed=response, ephemeral=ephemeral)
    else:
        content, embed = response
        await context.respond(content=content, embed=embed, ephemeral=ephemeral)
