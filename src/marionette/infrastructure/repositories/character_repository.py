import typing as t
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from marionette.application.protocols import CharacterRepository
from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles

from marionette.domain.statuses import CharacterStatus


class SqlAlchemyCharacterRepository(CharacterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @t.override
    def create(
        self,
        user_id: int,
        name: str,
        role: Roles,
        birthday: datetime,
        biography: str
    ) -> Character | None:
        character = Character(
            user_id=user_id,
            name=name,
            role=role,
            birthday=birthday,
            biography=biography
        )
        self._session.add(character)
        return character

    @t.override
    async def get_by_user_id_and_name(self, user_id: int, name: str) -> Character | None:
        stmt = (
            select(Character)
            .options(joinedload(Character.agency))
            .where(Character.name == name, Character.user_id == user_id)
        )
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]

    @t.override
    async def get_by_character_id(self, character_id: int) -> Character | None:
        stmt = (
            select(Character)
            .options(joinedload(Character.agency))
            .where(Character.id == character_id)
        )
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]

    @t.override
    async def get_all_characters_by_user_id(self, user_id: int) -> Sequence[Character]:
        stmt = (
            select(Character)
            .options(joinedload(Character.agency))
            .where(Character.user_id == user_id)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    @t.override
    async def get_active_characters_by_user_id(self, user_id: int) -> Sequence[Character]:
        stmt = (
            select(Character)
            .options(joinedload(Character.agency))
            .where(Character.user_id == user_id, Character.status == CharacterStatus.IS_ACTIVE)
        )
        result = await self._session.scalars(stmt)
        return result.all()

    @t.override
    async def get_entered_character_by_user_id(self, user_id: int) -> Character | None:
        stmt = (
            select(Character)
            .options(joinedload(Character.agency))
            .where(Character.user_id == user_id, Character.entered_channel_id.is_not(None))
        )
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]

    @t.override
    async def get_all(self) -> Sequence[Character]:
        stmt = select(Character).options(joinedload(Character.agency))
        result = await self._session.scalars(stmt)
        return result.all()

    @t.override
    async def delete(self, character: Character) -> None:
        await self._session.delete(character)
