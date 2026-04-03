from collections.abc import Callable

import pytest

from marionette.application.usecases.season_reset_usecase import SeasonResetUseCase
from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from tests.fakes import FakeAgencyRepository, FakeCharacterRepository, FakeTransaction


@pytest.mark.asyncio
async def test_execute_resets_ratings_to_expected_floor_by_band(
    character_factory: Callable[..., Character],
    agency_factory: Callable[..., Agency],
    fake_transaction: FakeTransaction,
) -> None:
    character_repo = FakeCharacterRepository(
        [
            character_factory(id=index + 1, name=f"Character {index}", rating=rating)
            for index, rating in enumerate(
                [0, 99, 100, 299, 300, 499, 500, 699, 700, 899, 900, 999, 1000]
            )
        ]
    )
    agency_repo = FakeAgencyRepository(
        [
            agency_factory(id=index + 1, owner_id=index + 1, name=f"Agency {index}", rating=rating)
            for index, rating in enumerate([150, 350, 650, 950, 1300])
        ]
    )

    await SeasonResetUseCase(
        character_repo=character_repo,
        agency_repo=agency_repo,
        transaction=fake_transaction,
    ).execute()

    assert [entity.rating for entity in character_repo.characters] == [
        0,
        0,
        25,
        25,
        70,
        70,
        150,
        150,
        200,
        200,
        300,
        300,
        400,
    ]
    assert [entity.rating for entity in agency_repo.agencies] == [25, 70, 150, 300, 400]
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0
