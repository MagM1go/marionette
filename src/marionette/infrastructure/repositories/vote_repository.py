import typing as t
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from marionette.application.protocols import VoteRepository
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.vote import Vote


class SqlAlchemyVoteRepository(VoteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @t.override
    def create(self, character_id: CharacterId, vote_time: datetime, voted_by: UserId) -> Vote:
        vote = Vote(character_id=character_id, voted_at=vote_time, voted_by=voted_by)
        self._session.add(vote)
        return vote

    @t.override
    async def get_vote_by_character_id(self, character_id: CharacterId) -> Vote | None:
        stmt = select(Vote).where(Vote.character_id == character_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
