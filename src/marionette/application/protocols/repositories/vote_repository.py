from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.vote import Vote, VoteSource


class VoteRepository(Protocol):
    """Хранилище голосов за персонажей."""

    def create(
        self,
        character_id: CharacterId,
        vote_time: datetime,
        voted_by: UserId,
        reputation: int = 1,
        source: VoteSource = VoteSource.COMMAND,
        perfomance_id: int | None = None,
        obtained: bool = False
    ) -> Vote:
        """Создаёт запись о голосе за персонажа.

        Args:
            character_id: ID персонажа, за которого проголосовали.
            vote_time: Время голоса.
            voted_by: Discord ID пользователя, который проголосовал.
            reputation: Количество получаемой репутации.
            source: Источник голоса.
            perfomance_id: ID публикации (выступления), за которую отдан голос.
            obtained: Была ли выдана репутация за голос.
        """
        ...

    async def get_votes_by_character_id(self, character_id: CharacterId) -> Sequence[Vote]:
        """Возвращает все голоса по персонажу."""
        ...

    async def get_vote_by_voter_and_perfomance_id(self, voted_by: UserId, perfomance_id: int) -> Vote | None:
        """Возвращает голос пользователя за публикацию, если он уже существует."""
        ...
