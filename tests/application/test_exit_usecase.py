from collections.abc import Callable

import pytest

from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import (
    CharacterNotEntranced,
    CharacterNotFound,
    WrongChannel,
)
from tests.fakes import FakeCharacterRepository


@pytest.mark.asyncio
async def test_execute_clears_location_on_success(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
) -> None:
    character = character_factory(entranced_channel_id=777)
    repo = character_repo_factory([character])

    result = await ExitUseCase(repo).execute(100, "Airi", 777)

    assert result.location_id == 777
    assert character.entranced_channel_id is None
    assert repo.set_location_calls == [(character, None)]


@pytest.mark.asyncio
async def test_execute_raises_when_character_missing(
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory()

    with pytest.raises(CharacterNotFound):
        await ExitUseCase(repo).execute(100, "Airi", 777)


@pytest.mark.asyncio
async def test_execute_raises_when_character_not_entranced(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory()])

    with pytest.raises(CharacterNotEntranced):
        await ExitUseCase(repo).execute(100, "Airi", 777)


@pytest.mark.asyncio
async def test_execute_raises_when_trying_to_exit_wrong_channel(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entranced_channel_id=321)])

    with pytest.raises(WrongChannel):
        await ExitUseCase(repo).execute(100, "Airi", 777)
