from collections.abc import Callable
from unittest.mock import Mock

import pytest

from marionette.application.protocols.types import UserId
from marionette.application.usecases.vote_usecase import VoteUseCase
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterNotFound
from marionette.domain.services.rating_service import RatingChangeReason
from tests.fakes import FakeCharacterRepository, FakeTransaction


@pytest.mark.asyncio
async def test_vote_for_increases_character_rating(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(rating=20)
    repo = character_repo_factory([character])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 7

    await VoteUseCase(
        rating_service=rating_service,
        character_repo=repo,
        transaction=fake_transaction,
    ).vote_for(UserId(100), "Airi")

    assert character.rating == 27
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
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(rating=20, agency_id=5)
    repo = character_repo_factory([character])
    rating_service = Mock()
    rating_service.inc_character_rating.return_value = 3

    await VoteUseCase(
        rating_service=rating_service,
        character_repo=repo,
        transaction=fake_transaction,
    ).vote_for(UserId(100), "Airi")

    assert character.rating == 23
    rating_service.inc_character_rating.assert_called_once_with(
        rating=5,
        reason=RatingChangeReason.VOTE,
        in_agency=True,
    )
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_vote_for_raises_when_character_missing(
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    repo = character_repo_factory([])
    rating_service = Mock()

    with pytest.raises(CharacterNotFound) as error:
        await VoteUseCase(
            rating_service=rating_service,
            character_repo=repo,
            transaction=fake_transaction,
        ).vote_for(UserId(100), "Airi")

    assert error.value.name == "Airi"
    rating_service.inc_character_rating.assert_not_called()
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
