import typing as t
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from marionette.application.protocols import VoteRepository
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.character import Character
from marionette.domain.entities.vote import Vote, VoteSource


class SqlAlchemyVoteRepository(VoteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @t.override
    def create(
        self,
        character_id: CharacterId,
        vote_time: datetime,
        voted_by: UserId,
        reputation: int = 1,
        source: VoteSource = VoteSource.COMMAND,
        perfomance_id: int | None = None,
        obtained: bool = False,
    ) -> Vote:
        vote = Vote(
            character_id=character_id,
            voted_at=vote_time,
            voted_by=voted_by,
            reputation=reputation,
            source=source,
            perfomance_id=perfomance_id,
            obtained=obtained,
        )
        self._session.add(vote)
        return vote

    @t.override
    async def get_votes_by_character_id(self, character_id: CharacterId) -> Sequence[Vote]:
        stmt = select(Vote).where(Vote.character_id == character_id)
        result = await self._session.scalars(stmt)
        return result.all()

    @t.override
    async def get_vote_by_voter_and_perfomance_id(self, voted_by: UserId, perfomance_id: int) -> Vote | None:
        stmt = select(Vote).where(Vote.voted_by == voted_by, Vote.perfomance_id == perfomance_id).limit(1)
        result = await self._session.scalars(stmt)
        return result.first()

    @t.override
    async def get_not_obtained_perfomance_votes(self) -> Sequence[tuple[Character, Vote]]:
        stmt = select(Character, Vote).join(Vote, Vote.character_id == Character.id).where(Vote.source == VoteSource.REVIEW, Vote.obtained.is_(False))
        result = await self._session.scalars(stmt)
        return result.all()
