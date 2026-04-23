from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
import itertools
import sys
import typing as t

import hikari
import miru
from miru.context.modal import ModalContext


class ModalItemV2(miru.abc.ModalItem, ABC):
    @abstractmethod
    def build_modal_component(self) -> t.Any:
        raise NotImplementedError

    def _build(self, action_row: hikari.api.ModalActionRowBuilder) -> None:
        raise RuntimeError(
            f"{type(self).__name__} is a modal v2 item and cannot be built into ModalActionRowBuilder"
        )


class ModalV2(miru.Modal):
    def build(self) -> t.Sequence[t.Any]:
        if not self.children:
            return []

        self._children.sort(
            key=lambda i: i._rendered_row if i._rendered_row is not None else sys.maxsize
        )

        components: list[t.Any] = []

        for _, items in itertools.groupby(self.children, lambda i: i._rendered_row):
            s_items = sorted(
                items, key=lambda i: i.position if i.position is not None else sys.maxsize
            )

            v2_items = [item for item in s_items if isinstance(item, ModalItemV2)]
            legacy_items = [item for item in s_items if not isinstance(item, ModalItemV2)]

            if v2_items and legacy_items:
                raise RuntimeError(
                    "Cannot mix legacy modal items and v2 modal items in the same row"
                )

            if v2_items:
                for v2_item in v2_items:
                    components.append(v2_item.build_modal_component())
                continue

            action_row = self._builder()
            for legacy_item in s_items:
                legacy_item._build(action_row)
            components.append(action_row)

        return components

    @staticmethod
    def _iter_submitted_components(
        components: t.Sequence[t.Any],
    ) -> t.Iterator[t.Any]:
        for component in components:
            if hasattr(component, "components"):
                yield from component.components
                continue

            nested_component = getattr(component, "component", None)
            if nested_component is not None:
                yield nested_component

    @staticmethod
    def _get_component_value(component: t.Any) -> str | tuple[str, ...] | None:
        value = getattr(component, "value", hikari.UNDEFINED)
        if value is not hikari.UNDEFINED:
            return t.cast(str, value)

        values = getattr(component, "values", hikari.UNDEFINED)
        if values is hikari.UNDEFINED:
            return None

        if isinstance(values, str):
            return values

        normalized = tuple(str(item) for item in values)
        if not normalized:
            return ""

        return normalized[0] if len(normalized) == 1 else normalized

    async def _invoke(
        self,
        interaction: hikari.ModalInteraction,
    ) -> asyncio.Future[t.Any] | None:
        children = {item.custom_id: item for item in self.children}
        values: dict[miru.abc.ModalItem, str | tuple[str, ...]] = {}

        for component in self._iter_submitted_components(interaction.components):
            custom_id = getattr(component, "custom_id", None)
            if custom_id is None:
                continue

            child = children.get(custom_id)
            if child is None:
                continue

            value = self._get_component_value(component)
            if value is None:
                continue

            values[child] = value

        if not values:
            return None

        self._values = values  # type: ignore[assignment]

        context = ModalContext(
            self,
            self.client,
            interaction,
            values,  # type: ignore[arg-type]
        )
        self._last_context = context

        passed = await self.modal_check(context)
        if not passed:
            return None

        for item in self.children:
            await item._refresh_state(context)

        self._create_task(self._handle_callback(context))

        if self.client.is_rest:
            return context._resp_builder

        return None
