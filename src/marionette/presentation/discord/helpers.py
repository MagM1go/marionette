from collections.abc import Mapping, Sequence
import typing as t


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
