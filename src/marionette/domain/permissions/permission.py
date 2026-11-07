from typing import Protocol


class Permission(Protocol):
    @staticmethod
    def code() -> str: ...
