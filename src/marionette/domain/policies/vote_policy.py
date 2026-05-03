from datetime import datetime, timedelta

from marionette.domain.entities.character import Character
from marionette.domain.entities.vote import Vote
from marionette.domain.exceptions import CharacterNotFound


class VotePolicy:
    VOTE_COOLDOWN = timedelta(hours=6)

    @staticmethod
    def ensure_character_exists(character: Character | None, expected_name: str) -> None:
        if character is None:
            raise CharacterNotFound(name=expected_name)

    @staticmethod
    def is_on_cooldown(vote: Vote, now: datetime) -> bool:
        return now < vote.voted_at + VotePolicy.VOTE_COOLDOWN

    @staticmethod
    def cooldown_remaining(vote: Vote, now: datetime) -> timedelta:
        return max((vote.voted_at + VotePolicy.VOTE_COOLDOWN) - now, timedelta(0))
