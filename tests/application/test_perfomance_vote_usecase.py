from collections.abc import Callable
from datetime import UTC, datetime

from marionette.domain.services.rating_service import RatingService
import pytest

from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.character import Character
from marionette.domain.entities.vote import Vote, VoteSource
from marionette.domain.exceptions import AlreadyVotedForPerfomance, CanNotVoteYourself, CharacterNotFound
from marionette.application.usecases.vote.perfomance_vote_usecase import PerfomanceVoteUseCase
from tests.fakes import FakeCharacterRepository, FakeTransaction, FakeVoteRepository


@pytest.mark.asyncio
async def test_vote_creates_positive_review_vote(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=10, user_id=101)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)

    await PerfomanceVoteUseCase(
        transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService(roll=lambda low, high: 8)
    ).vote(character_id=CharacterId(10), voted_by=UserId(200), now=now, reputation=1, perfomance_id=1_000)

    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].character_id == 10
    assert vote_repo.votes[0].voted_by == 200
    assert vote_repo.votes[0].voted_at == now
    assert vote_repo.votes[0].reputation == 6
    assert character.reputation == 100
    assert vote_repo.votes[0].source == VoteSource.REVIEW
    assert vote_repo.votes[0].perfomance_id == 1_000
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_creates_negative_review_vote(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=10, user_id=101)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)

    await PerfomanceVoteUseCase(
        transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
    ).vote(character_id=CharacterId(10), voted_by=UserId(200), now=now, reputation=-1, perfomance_id=1_000)

    assert len(vote_repo.votes) == 1
    assert vote_repo.votes[0].reputation == -1
    assert character.reputation == 100
    assert vote_repo.votes[0].source == VoteSource.REVIEW
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_raises_when_voting_for_own_perfomance(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=10, user_id=101)
    repo = character_repo_factory([character])
    vote_repo = vote_repo_factory(None)

    with pytest.raises(CanNotVoteYourself):
        await PerfomanceVoteUseCase(
            transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
        ).vote(character_id=CharacterId(10), voted_by=UserId(101), now=now, reputation=1, perfomance_id=1_000)

    assert len(vote_repo.votes) == 0
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_raises_when_character_missing(
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    repo = character_repo_factory([])
    vote_repo = vote_repo_factory(None)

    with pytest.raises(CharacterNotFound) as error:
        await PerfomanceVoteUseCase(
            transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
        ).vote(character_id=CharacterId(42), voted_by=UserId(200), now=now, reputation=1, perfomance_id=1_000)

    assert error.value.name == "42"
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_raises_when_already_voted_for_same_perfomance(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    """Повторный голос за ту же публикацию невозможен, даже мгновенно."""
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=10, user_id=101)
    repo = character_repo_factory([character])
    existing_vote = vote_factory(character_id=10, voted_by=200, voted_at=now, source=VoteSource.REVIEW, perfomance_id=1_000)
    vote_repo = vote_repo_factory([existing_vote])

    with pytest.raises(AlreadyVotedForPerfomance):
        await PerfomanceVoteUseCase(
            transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
        ).vote(character_id=CharacterId(10), voted_by=UserId(200), now=now, reputation=1, perfomance_id=1_000)

    assert len(vote_repo.votes) == 1
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_raises_when_same_user_votes_for_another_character_in_same_perfomance(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    """Один голос на пользователя на публикацию: другой персонаж той же публикации тоже закрыт."""
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=11, user_id=102)
    repo = character_repo_factory([character])
    existing_vote = vote_factory(character_id=10, voted_by=200, voted_at=now, source=VoteSource.REVIEW, perfomance_id=1_000)
    vote_repo = vote_repo_factory([existing_vote])

    with pytest.raises(AlreadyVotedForPerfomance):
        await PerfomanceVoteUseCase(
            transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
        ).vote(character_id=CharacterId(11), voted_by=UserId(200), now=now, reputation=1, perfomance_id=1_000)

    assert len(vote_repo.votes) == 1
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_vote_allows_same_character_in_another_perfomance(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    vote_factory: Callable[..., Vote],
    vote_repo_factory: Callable[[list[Vote] | None], FakeVoteRepository],
    fake_transaction: FakeTransaction,
) -> None:
    """За того же персонажа в другой публикации голосовать можно."""
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    character = character_factory(id=10, user_id=101)
    repo = character_repo_factory([character])
    existing_vote = vote_factory(character_id=10, voted_by=200, voted_at=now, source=VoteSource.REVIEW, perfomance_id=1_000)
    vote_repo = vote_repo_factory([existing_vote])

    await PerfomanceVoteUseCase(
        transaction=fake_transaction, vote_repository=vote_repo, character_repository=repo, ranking=RatingService()
    ).vote(character_id=CharacterId(10), voted_by=UserId(200), now=now, reputation=1, perfomance_id=2_000)

    assert len(vote_repo.votes) == 2
    assert vote_repo.votes[1].perfomance_id == 2_000
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
