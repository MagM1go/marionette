from datetime import datetime

from marionette.application.protocols import CharacterRepository, VoteRepository
from marionette.application.protocols.repositories.subscription_repository import SubscriptionRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.vote import VoteSource
from marionette.domain.exceptions import CanNotVoteYourself, MustBeSubscribed, VoteOnCooldown
from marionette.domain.policies.character_policy import CharacterPolicy
from marionette.domain.policies.vote_policy import VotePolicy
from marionette.domain.services.rating_service import RatingChangeReason, RatingService


class VoteUseCase:
    def __init__(
        self,
        rating_service: RatingService,
        character_repo: CharacterRepository,
        vote_repo: VoteRepository,
        subscription_repo: SubscriptionRepository,
        transaction: Transaction,
    ) -> None:
        self._rating_service = rating_service
        self._character_repository = character_repo
        self._vote_repository = vote_repo
        self._subscription_repository = subscription_repo
        self._transaction = transaction

    async def vote_for(self, voted_by: UserId, user_id: UserId, character_name: str, now: datetime) -> None:
        if voted_by == user_id:
            raise CanNotVoteYourself()

        async with self._transaction:
            character = await self._character_repository.get_by_user_id_and_name(user_id=user_id, name=character_name)
            CharacterPolicy.ensure_character_exists(character, character_name)

            assert character is not None
            VotePolicy.ensure_character_is_applied(character, character_name)

            subscription = await self._subscription_repository.get_follower_subscription_by_character(voted_by, CharacterId(character.id))
            if subscription is None:
                raise MustBeSubscribed()

            votes = await self._vote_repository.get_votes_by_character_id(character_id=CharacterId(character.id))
            increased_reputation = self._rating_service.inc_character_rating(
                rating=character.reputation,
                reason=RatingChangeReason.VOTE,
                in_agency=character.agency_id is not None,
            )
            
            user_command_vote = next((vote for vote in votes if vote.source == VoteSource.COMMAND), None)
            if user_command_vote is None:
                user_command_vote = self._vote_repository.create(
                    character_id=CharacterId(character.id),
                    vote_time=now,
                    voted_by=voted_by,
                    reputation=increased_reputation - character.reputation,
                )
            else:
                if VotePolicy.is_on_cooldown(vote=user_command_vote, now=now):
                    raise VoteOnCooldown(character.name, VotePolicy.cooldown_remaining(vote=user_command_vote, now=now))
                    
                user_command_vote.voted_at = now
                
            character.reputation = increased_reputation
            await self._transaction.commit()
