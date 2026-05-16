from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from marionette.application.protocols.types import UserId
from marionette.application.usecases.vote_usecase import VoteUseCase
from marionette.domain.entities.character import Character
from marionette.domain.entities.vote import Vote
from marionette.domain.exceptions import CharacterNotFound, VoteOnCooldown
from marionette.domain.services.rating_service import RatingChangeReason
from tests.fakes import FakeCharacterRepository, FakeTransaction, FakeVoteRepository


@pytest.mark.asyncio
async def test_vote_for_increases_character_rating(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, rating=20)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 7

    await VoteUseCase(
        rating_service=rating_service,
        character_repo=repo,
        vote_repo=vote_repo,
        transaction=fake_transaction,
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.rating == 27
    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].character_id == character.id
    assert vote_repo.votes[0].voted_by == 100
    assert vote_repo.votes[0].voted_at == now
    rating_service.inc_character_rating.assert_called_once_with(
        rating=5,
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
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, rating=20, agency_id=3)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 3

    await VoteUseCase(
        rating_service=rating_service,
        character_repo=repo,
        vote_repo=vote_repo,
        transaction=fake_transaction,
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.rating == 23
    rating_service.inc_character_rating.assert_called_once_with(
        rating=5,
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
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, rating=20)
    vote = vote_factory(character_id=10, voted_by=999, voted_at=now - timedelta(hours=1))
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory([vote])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 7

    with pytest.raises(VoteOnCooldown) as error:
        await VoteUseCase(
            rating_service=rating_service,
            character_repo=repo,
            vote_repo=vote_repo,
            transaction=fake_transaction,
        ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert error.value.character_name == "Airi"
    assert error.value.remaining_time == timedelta(hours=23)
    assert character.rating == 20
    assert len(vote_repo.votes) == 1
    rating_service.inc_character_rating.assert_not_called()
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_for_updates_existing_vote_after_cooldown(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(user_id=101, rating=20)
    vote = vote_factory(character_id=10, voted_by=999, voted_at=now - timedelta(hours=25))
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory([vote])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 4

    await VoteUseCase(
        rating_service=rating_service,
        character_repo=repo,
        vote_repo=vote_repo,
        transaction=fake_transaction,
    ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert character.rating == 24
    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].voted_at == now
    assert vote_repo.votes[0].voted_by == 100
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_raises_when_character_missing(
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    repo = character_repo_factory([])
    vote_repo = vote_repo_factory([])
    rating_service = Mock()

    with pytest.raises(CharacterNotFound) as error:
        await VoteUseCase(
            rating_service=rating_service,
            character_repo=repo,
            vote_repo=vote_repo,
            transaction=fake_transaction,
        ).vote_for(UserId(100), UserId(101), "Airi", now)

    assert error.value.name == "Airi"
    rating_service.inc_character_rating.assert_not_called()
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
