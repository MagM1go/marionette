import typing as t

import hikari
import miru
from hikari.api.special_endpoints import LabelComponentBuilder as LabelComponentBuilderApi
from hikari.impl import special_endpoints

from marionette.presentation.discord.ui.wrapper.modal_v2 import ModalItemV2


class TextInputExtension(ModalItemV2, miru.TextInput):
    """Extending to V2 TextInput"""

    @t.override
    def build_modal_component(self) -> LabelComponentBuilderApi:
        text_input = special_endpoints.TextInputBuilder(
            custom_id=self.custom_id,
            style=self.style,
            placeholder=self.placeholder or hikari.UNDEFINED,
            value=self.value or hikari.UNDEFINED,
            required=self.required,
            min_length=self.min_length or 0,
            max_length=self.max_length or 1024,
        )
        return special_endpoints.LabelComponentBuilder(label=self.label, component=text_input)
