from enum import StrEnum


class CharacterStatus(StrEnum):
    IS_ACTIVE = "active"
    """Персонаж играбелен. Не путать с `Character.is_active`."""
    
    ABANDONED = "abandoned"
    MODERATION = "moderation"
