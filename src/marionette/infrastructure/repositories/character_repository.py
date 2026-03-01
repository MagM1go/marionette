import typing as t
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.domain.entities.character import Character
from marionette.domain.repositories import ICharacterRepository
from marionette.domain.roles import Roles


class CharacterRepository(ICharacterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    @t.override
    async def save(
        self, user_id: int, name: str, role: Roles, birthday: datetime, home_channel_id: int
    ) -> Character | None:
        try:
            character = Character(
                user_id=user_id, name=name, role=role, birthday=birthday, home_channel_id=home_channel_id
            )
            self.session.add(character)
            await self.session.flush()
            return character
        except IntegrityError:
            await self.session.rollback()
            return None

    @t.override
    async def update(self) -> None:
        await self.session.flush()

    @t.override
    async def set_active(self, user_id: int, name: str, is_active: bool) -> None:
        await self.session.execute(
            update(Character)
            .where(Character.user_id == user_id, Character.name == name)
            .values(is_active=is_active)
        )
        
    @t.override
    async def set_timeline(self, character: Character, channel_id: int | None) -> None:
        await self.session.execute(
            update(Character)
            .where(Character.id == character.id)
            .values(entranced_channel_id=channel_id)
        )

    @t.override
    async def get_by_user_id_and_name(
        self, user_id: int, name: str
    ) -> Character | None:
        stmt = select(Character).where(
            Character.name == name, Character.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @t.override
    async def get_by_character_id(self, character_id: int) -> Character | None:
        stmt = select(Character).where(Character.id == character_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @t.override
    async def get_all_characters_by_user_id(self, user_id: int) -> Sequence[Character]:
        stmt = select(Character).where(Character.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
        
    @t.override
    async def get_entranced_character_by_user_id(self, user_id: int) -> Character | None:
        stmt = select(Character).where(
            Character.user_id == user_id, 
            Character.entranced_channel_id.is_not(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @t.override
    async def get_all(self) -> Sequence[Character]:
        stmt = select(Character)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @t.override
    async def delete_by_name_and_user_id(self, name: str, user_id: int) -> bool:
        character = await self.get_by_user_id_and_name(user_id, name)

        if character:
            await self.session.delete(character)
            await self.session.flush()
            return True

        return False
