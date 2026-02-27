from dataclasses import dataclass

from marionette.application.dto.embed import Embed


@dataclass
class Result:
    content: str | None = None
    embed: Embed | None = None

    def is_empty(self) -> bool:
        return not self.content and not self.embed
