from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterNotInLocation


@pytest.mark.asyncio
async def test_expose_raises_when_character_not_in_location(
    character_factory: Callable[..., Character],
) -> None:
    character = character_factory()
    character.entranced_channel_id = None
    usecase = PaparazziUseCase(rating_service=Mock())

    with pytest.raises(CharacterNotInLocation):
        await usecase.expose(character)


@pytest.mark.asyncio
async def test_expose_returns_none_when_on_cooldown(
    character_factory: Callable[..., Character],
) -> None:
    last_exposure = datetime.now(UTC) - timedelta(hours=1)
    character = character_factory(entranced_channel_id=777, last_exposed_at=last_exposure)

    rating_service = Mock()
    usecase = PaparazziUseCase(rating_service=rating_service)

    result = await usecase.expose(character)

    assert result is None
    rating_service.dec_character_rating.assert_not_called()


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.3)
async def test_expose_works_after_cooldown_expired(
    _: object, character_factory: Callable[..., Character]
) -> None:
    # Прошло 25 часов
    expired_exposure = datetime.now(UTC) - timedelta(hours=25)
    character = character_factory(entranced_channel_id=777, last_exposed_at=expired_exposure)

    rating_service = Mock()
    rating_service.dec_character_rating.return_value = 100
    usecase = PaparazziUseCase(rating_service=rating_service)

    result = await usecase.expose(character)

    assert result is not None
    assert character.rating == 100


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.3)
async def test_expose_updates_last_exposed_at_timestamp(
    _: object, character_factory: Callable[..., Character]
) -> None:
    character = character_factory(entranced_channel_id=777, last_exposed_at=None)
    rating_service = Mock()
    rating_service.dec_character_rating.return_value = character.rating
    usecase = PaparazziUseCase(rating_service=rating_service)

    await usecase.expose(character)

    assert character.last_exposed_at is not None
    assert (datetime.now(UTC) - character.last_exposed_at).total_seconds() < 10


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.1)
async def test_expose_returns_none_when_roll_outside_chance(
    _: object, character_factory: Callable[..., Character]
) -> None:
    rating_service = Mock()
    usecase = PaparazziUseCase(rating_service=rating_service)

    result = await usecase.expose(character_factory(entranced_channel_id=777))

    assert result is None
    rating_service.dec_character_rating.assert_not_called()


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.3)
async def test_expose_updates_character_and_agency_ratings(
    _: object, agency_factory: Callable[..., Agency], character_factory: Callable[..., Character]
) -> None:
    agency = agency_factory(rating=400)
    character = character_factory(
        rating=120,
        entranced_channel_id=777,
        agency=agency,
    )
    rating_service = Mock()
    rating_service.dec_character_rating.return_value = 100
    rating_service.dec_agency_rating_from_member.return_value = 392
    usecase = PaparazziUseCase(rating_service=rating_service)

    result = await usecase.expose(character)

    assert result is not None
    assert result.exposed_character_name == "Airi"
    assert result.expose_channel_id == 777
    assert character.rating == 100
    assert agency.rating == 392
    rating_service.dec_character_rating.assert_called_once()
    rating_service.dec_agency_rating_from_member.assert_called_once_with(
        agency_rating=400,
        character_loss=20,
    )
