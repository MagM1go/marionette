import typing as t

import attrs
import hikari
import miru
from hikari.impl import entity_factory as hikari_entity_factory
from hikari.impl import special_endpoints as hikari_impl
from miru.context.modal import ModalContext

from marionette.presentation.discord.ui.wrapper.modal_v2 import ModalItemV2

__all__ = ("StringSelect",)


@attrs.define(kw_only=True, weakref_slot=False)
class _TextSelectMenuComponentWithValues(hikari.TextSelectMenuComponent):
    values: tuple[str, ...] = attrs.field(factory=tuple)


_TEXT_SELECT_DESERIALIZER_PATCHED = False

if not _TEXT_SELECT_DESERIALIZER_PATCHED:
    _ORIGINAL_DESERIALIZE_TEXT_SELECT_MENU = (
        hikari_entity_factory.EntityFactoryImpl._deserialize_text_select_menu
    )

    def _deserialize_text_select_menu_with_values(
        self: hikari_entity_factory.EntityFactoryImpl,
        payload: t.Mapping[str, t.Any],
    ) -> hikari.TextSelectMenuComponent:
        component = _ORIGINAL_DESERIALIZE_TEXT_SELECT_MENU(self, payload)
        raw_values = payload.get("values")

        if raw_values is None:
            return component

        return _TextSelectMenuComponentWithValues(
            type=component.type,
            id=component.id,
            custom_id=component.custom_id,
            placeholder=component.placeholder,
            min_values=component.min_values,
            max_values=component.max_values,
            is_disabled=component.is_disabled,
            options=component.options,
            values=tuple(str(value) for value in raw_values),
        )

    hikari_entity_factory.EntityFactoryImpl._deserialize_text_select_menu = (  # type: ignore[method-assign]
        _deserialize_text_select_menu_with_values
    )
    _TEXT_SELECT_DESERIALIZER_PATCHED = True


class StringSelect(ModalItemV2):
    def __init__(
        self,
        *,
        label: str,
        options: t.Sequence[miru.SelectOption],
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        required: bool = True,
        custom_id: str | None = None,
        row: int | None = None,
    ) -> None:
        super().__init__(custom_id=custom_id, row=row, position=0, width=5, required=required)
        self.label = label
        self.options = list(options)
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self._values: tuple[str, ...] = ()

    @property
    def type(self) -> hikari.ComponentType:
        return hikari.ComponentType.TEXT_SELECT_MENU

    @property
    def values(self) -> tuple[str, ...]:
        return self._values

    @property
    def value(self) -> str | None:
        return self._values[0] if self._values else None

    def build_modal_component(self) -> t.Any:
        menu = hikari_impl.TextSelectMenuBuilder(
            custom_id=self.custom_id,
            placeholder=self.placeholder or hikari.UNDEFINED,
            min_values=self.min_values,
            max_values=self.max_values,
            is_required=self.required,
        )

        for option in self.options:
            menu.add_option(
                option.label,
                option.value,
                description=getattr(option, "description", hikari.UNDEFINED) or hikari.UNDEFINED,
                emoji=getattr(option, "emoji", hikari.UNDEFINED) or hikari.UNDEFINED,
                is_default=getattr(option, "is_default", False),
            )

        return hikari_impl.LabelComponentBuilder(
            label=self.label,
            component=menu,
        )

    async def _refresh_state(self, context: ModalContext) -> None:
        raw = context.values.get(self)

        if raw is None:
            self._values = ()
        elif isinstance(raw, str):
            self._values = (raw,)
        else:
            self._values = tuple(raw)
