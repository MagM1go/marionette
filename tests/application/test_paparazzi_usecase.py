from collections.abc import Callable
from unittest.mock import Mock, patch

import pytest

from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterNotInLocation
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from tests.fakes import FakeCooldownRepository


@pytest.mark.asyncio
async def test_expose_raises_when_character_not_in_location(
    character_factory: Callable[..., Character],
) -> None:
    character = character_factory()
    character.entranced_channel_id = None
    usecase = PaparazziUseCase(
        rating_service=Mock(),
        cooldown_repo=FakeCooldownRepository(),
    )

    with pytest.raises(CharacterNotInLocation):
        await usecase.expose(character)


@pytest.mark.asyncio
async def test_expose_returns_none_when_on_cooldown(
    character_factory: Callable[..., Character],
    cooldown_repo_factory: Callable[..., FakeCooldownRepository],
) -> None:
    rating_service = Mock()
    cooldown_repo = cooldown_repo_factory(True)
    usecase = PaparazziUseCase(rating_service=rating_service, cooldown_repo=cooldown_repo)

    result = await usecase.expose(character_factory(entranced_channel_id=777))

    assert result is None
    rating_service.dec_character_rating.assert_not_called()
    assert cooldown_repo.set_calls == []


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.1)
async def test_expose_returns_none_when_roll_outside_chance(
    _: object,
    character_factory: Callable[..., Character],
    cooldown_repo_factory: Callable[..., FakeCooldownRepository],
) -> None:
    rating_service = Mock()
    cooldown_repo = cooldown_repo_factory()
    usecase = PaparazziUseCase(rating_service=rating_service, cooldown_repo=cooldown_repo)

    result = await usecase.expose(character_factory(entranced_channel_id=777))

    assert result is None
    rating_service.dec_character_rating.assert_not_called()
    assert cooldown_repo.set_calls == []


@pytest.mark.asyncio
@patch("marionette.application.usecases.paparazzi_usecase.random.random", return_value=0.3)
async def test_expose_updates_character_and_agency_ratings(
    _: object,
    agency_factory: Callable[..., Agency],
    character_factory: Callable[..., Character],
    cooldown_repo_factory: Callable[..., FakeCooldownRepository],
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
    cooldown_repo = cooldown_repo_factory()
    usecase = PaparazziUseCase(rating_service=rating_service, cooldown_repo=cooldown_repo)

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
    assert cooldown_repo.set_calls == [("cooldown:100:10", PaparazziPolicy.ONE_DAY)]
