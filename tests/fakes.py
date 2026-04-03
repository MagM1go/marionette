from collections.abc import Sequence
from datetime import date, datetime
from types import TracebackType
from typing import Self

from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles


class FakeCharacterRepository:
    def __init__(self, characters: list[Character] | None = None) -> None:
        self.characters = characters or []

    def create(
        self,
        user_id: int,
        name: str,
        role: Roles,
        birthday: date | datetime,
        home_channel_id: int
    ) -> Character:
        birthday_datetime = (
            birthday
            if isinstance(birthday, datetime)
            else datetime.combine(birthday, datetime.min.time())
        )
        character = Character(
            id=len(self.characters) + 1,
            user_id=user_id,
            name=name,
            role=role,
            birthday=birthday_datetime,
            home_channel_id=home_channel_id,
            rating=0,
            is_active=False,
            is_in_performance=False,
            last_exposed_at=None
        )
        self.characters.append(character)
        return character

    async def get_all(self) -> Sequence[Character]:
        return self.characters

    async def set_active(self, user_id: int, name: str, is_active: bool) -> None:
        for character in self.characters:
            if character.user_id == user_id and character.name == name:
                character.is_active = is_active
                return

    async def get_by_user_id_and_name(self, user_id: int, name: str) -> Character | None:
        for character in self.characters:
            if character.user_id == user_id and character.name == name:
                return character
        return None

    async def get_all_characters_by_user_id(self, user_id: int) -> Sequence[Character]:
        return [character for character in self.characters if character.user_id == user_id]

    async def get_by_character_id(self, character_id: int) -> Character | None:
        for character in self.characters:
            if character.id == character_id:
                return character
        return None

    async def get_entranced_character_by_user_id(self, user_id: int) -> Character | None:
        for character in self.characters:
            if character.user_id == user_id and character.entranced_channel_id is not None:
                return character
        return None

    async def delete(self, character: Character) -> None:
        self.characters.remove(character)


class FakeAgencyRepository:
    def __init__(self, agencies: list[Agency] | None = None) -> None:
        self.agencies = agencies or []

    def create(self, owner_id: int, name: str) -> Agency:
        agency = Agency(
            id=len(self.agencies) + 1,
            owner_id=owner_id,
            name=name,
            rating=0,
        )
        self.agencies.append(agency)
        return agency

    async def get_all(self) -> Sequence[Agency]:
        return self.agencies

    async def get_agency_by_id(self, agency_id: int) -> Agency | None:
        for agency in self.agencies:
            if agency.id == agency_id:
                return agency
        return None


class FakeTransaction:
    def __init__(self) -> None:
        self.commit_calls = 0
        self.rollback_calls = 0

    async def commit(self) -> None:
        self.commit_calls += 1

    async def rollback(self) -> None:
        self.rollback_calls += 1

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc: BaseException | None = None,
        exc_traceback: TracebackType | None = None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
