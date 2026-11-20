from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from marionette.application.protocols.types import UserId
from marionette.application.usecases.vote.vote_usecase import VoteUseCase
from marionette.domain.entities.character import Character
from marionette.domain.entities.subscription import Subscription
from marionette.domain.entities.vote import Vote, VoteSource
from marionette.domain.exceptions import CharacterNotFound, VoteOnCooldown
from marionette.domain.services.rating_service import RatingChangeReason
from tests.fakes import FakeCharacterRepository, FakeSubscriptionRepository, FakeTransaction, FakeVoteRepository


@pytest.mark.asyncio
async def test_vote_for_increases_character_rating(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, reputation=20)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)
    subscription = subscription_factory(follower_id=100, character_author_id=101, character_id=character.id)
    subscription_repo = subscription_repo_factory([subscription])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 27

    await VoteUseCase(
        rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.reputation == 27
    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].character_id == character.id
    assert vote_repo.votes[0].voted_by == 100
    assert vote_repo.votes[0].voted_at == now
    assert vote_repo.votes[0].reputation == 7
    rating_service.inc_character_rating.assert_called_once_with(
        rating=20,
        reason=RatingChangeReason.VOTE,
        in_agency=False,
    )
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_passes_agency_flag_when_character_has_agency(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, reputation=20, agency_id=3)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)
    subscription = subscription_factory(follower_id=100, character_author_id=101, character_id=character.id)
    subscription_repo = subscription_repo_factory([subscription])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 23

    await VoteUseCase(
        rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.reputation == 23
    rating_service.inc_character_rating.assert_called_once_with(
        rating=20,
        reason=RatingChangeReason.VOTE,
        in_agency=True,
    )
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_raises_when_character_vote_is_on_global_cooldown(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, reputation=20)
    vote = vote_factory(character_id=10, voted_by=999, voted_at=now - timedelta(hours=1))
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory([vote])
    subscription = subscription_factory(follower_id=100, character_author_id=101, character_id=character.id)
    subscription_repo = subscription_repo_factory([subscription])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 27

    with pytest.raises(VoteOnCooldown) as error:
        await VoteUseCase(
            rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
        ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert error.value.character_name == "Airi"
    assert error.value.remaining_time == timedelta(hours=23)
    assert character.reputation == 20
    assert len(vote_repo.votes) == 1
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_for_updates_existing_vote_after_cooldown(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, reputation=20)
    vote = vote_factory(character_id=10, voted_by=999, voted_at=now - timedelta(hours=25))
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory([vote])
    subscription = subscription_factory(follower_id=100, character_author_id=101, character_id=character.id)
    subscription_repo = subscription_repo_factory([subscription])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 24
    await VoteUseCase(
        rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.reputation == 24
    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].voted_at == now
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_ignores_review_votes_for_cooldown(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    """Свежие отзывы выступлений (REVIEW) не включают кулдаун команды `/vote`."""
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, reputation=20)
    review_votes = [
        Vote(character_id=10, voted_by=100, voted_at=now, reputation=1, source=VoteSource.REVIEW),
        Vote(character_id=10, voted_by=201, voted_at=now, reputation=-1, source=VoteSource.REVIEW),
    ]
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(review_votes)
    subscription = subscription_factory(follower_id=100, character_author_id=101, character_id=character.id)
    subscription_repo = subscription_repo_factory([subscription])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 21

    await VoteUseCase(
        rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.reputation == 21
    assert len(vote_repo.votes) == 3
    assert vote_repo.votes[-1].source == VoteSource.COMMAND
    assert vote_repo.votes[-1].voted_by == 100
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_raises_when_character_missing(
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    subscription_factory: Callable[..., Subscription],
    subscription_repo_factory: Callable[[list[Subscription] | None], FakeSubscriptionRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    repo = character_repo_factory([])
    subscription_repo = subscription_repo_factory([])
    vote_repo = vote_repo_factory([])
    rating_service = Mock()

    with pytest.raises(CharacterNotFound) as error:
        await VoteUseCase(
            rating_service=rating_service, character_repo=repo, vote_repo=vote_repo, transaction=fake_transaction, subscription_repo=subscription_repo
        ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert error.value.name == "Airi"
    rating_service.inc_character_rating.assert_not_called()
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
