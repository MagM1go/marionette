import typing as t


class ModerationPolicy:
    NON_RP_PREFIXES: t.Final[list[str]] = ["//", "((", "OOC", "ООС"]

    @classmethod
    def should_delete_message(cls, message_content: str) -> bool:
        return not any(message_content.startswith(prefix) for prefix in cls.NON_RP_PREFIXES)
