import typing as t


class ModerationPolicy:
    NON_RP_PREFIX: t.Final[str] = "//"

    @classmethod
    def should_delete_message(cls, message_content: str) -> bool:
        return not message_content.startswith(cls.NON_RP_PREFIX)
