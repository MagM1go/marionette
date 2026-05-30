from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterAlreadyActive, CharacterIsAbandoned, CharacterNotFound
from marionette.domain.statuses import CharacterStatus


class CharacterPolicy:
    @staticmethod
    def ensure_character_exists(character: Character | None, expected_name: str) -> None:
        if character is None:
            raise CharacterNotFound(name=expected_name)

    @staticmethod
    def ensure_character_can_be_judged(character: Character) -> None:
        if character.status == CharacterStatus.ABANDONED:
            raise CharacterIsAbandoned()

        if character.status == CharacterStatus.IS_ACTIVE:
            raise CharacterAlreadyActive()
