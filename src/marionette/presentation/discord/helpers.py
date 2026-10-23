import typing as t
from collections.abc import Mapping, Sequence

import hikari

from marionette.bootstrap.config import config
from marionette.domain.roles import Roles

ROLEPLAY_ROLE_TO_DISCORD: t.Final[dict[Roles, int]] = {
    Roles.AGENT: config.discord.roles.agent,
    Roles.ACTOR: config.discord.roles.actor,
    Roles.IDOL: config.discord.roles.idol,
    Roles.LAWYER: config.discord.roles.lawyer,
    Roles.MANGAKA: config.discord.roles.mangaka,
    Roles.WRITER: config.discord.roles.writer,
    Roles.MEDICINE: config.discord.roles.medicine,
    Roles.STYLIST: config.discord.roles.stylist,
    Roles.EDITOR: config.discord.roles.editor,
    Roles.VIEWER: config.discord.roles.viewer,
}


class UserInterfaceHelper:
    @staticmethod
    def _iter_modal_components(modal_components: Sequence[t.Any]) -> t.Iterator[t.Any]:
        for item in modal_components:
            if hasattr(item, "components"):
                yield from item.components
                continue

            component = getattr(item, "component", None)
            if component is not None:
                yield component

    @staticmethod
    def _extract_value(component: t.Any) -> str | None:
        value = getattr(component, "value", None)
        if value is not None:
            return str(value)

        values = getattr(component, "values", None)
        if values is None:
            return None

        if isinstance(values, str):
            return values

        for item in values:
            return str(item)

        return ""

    @staticmethod
    def modal_map(modal_components: Sequence[t.Any]) -> dict[str, str]:
        return {
            component.custom_id: value
            for component in UserInterfaceHelper._iter_modal_components(modal_components)
            if getattr(component, "custom_id", None) is not None
            if (value := UserInterfaceHelper._extract_value(component)) is not None
        }

    @staticmethod
    def labeled_modal_map(modal_components: Sequence[t.Any]) -> dict[str, str]:
        return UserInterfaceHelper.modal_map(modal_components)

    @staticmethod
    def get_modal_value(modal: Mapping[str, str], custom_id: str) -> str:
        return modal.get(custom_id, "unresolved")


async def get_or_fetch_channel(rest: hikari.api.RESTClient, cache: hikari.api.Cache, channel_id: int) -> hikari.PartialChannel:
    if not (channel := cache.get_guild_channel(channel_id)):
        return await rest.fetch_channel(channel_id)

    return channel


def character_role_to_discod_role(role: Roles) -> hikari.Snowflakeish:
    return ROLEPLAY_ROLE_TO_DISCORD[role]
