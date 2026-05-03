from datetime import datetime
from typing import Protocol

from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.vote import Vote


class VoteRepository(Protocol):
    """Хранилище голосов за персонажей."""

    def create(self, character_id: CharacterId, vote_time: datetime, voted_by: UserId) -> Vote:
        """Создаёт запись о голосе за персонажа.

        Args:
            character_id: ID персонажа, за которого проголосовали.
            vote_time: Время голоса.
            voted_by: Discord ID пользователя, который проголосовал.
        """
        ...
