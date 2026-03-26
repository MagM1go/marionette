from collections.abc import Callable

import pytest

from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import (
    AlreadyInLocation,
    AnotherCharacterIsActive,
    CharacterNotFound,
)
from tests.fakes import FakeCharacterRepository


@pytest.mark.asyncio
async def test_execute_sets_location_for_character(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
) -> None:
    character = character_factory()
    repo = character_repo_factory([character])

    result = await EntranceUseCase(repo).execute(100, "Airi", 777)

    assert result.location_id == 777
    assert character.entranced_channel_id == 777
    assert repo.set_location_calls == [(character, 777)]


@pytest.mark.asyncio
async def test_execute_raises_when_character_missing(
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory()

    with pytest.raises(CharacterNotFound):
        await EntranceUseCase(repo).execute(100, "Airi", 777)


@pytest.mark.asyncio
async def test_execute_raises_when_character_already_entranced(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entranced_channel_id=321)])

    with pytest.raises(AlreadyInLocation):
        await EntranceUseCase(repo).execute(100, "Airi", 777)


@pytest.mark.asyncio
async def test_execute_raises_when_another_character_is_active(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    target = character_factory(name="Airi")
    active = character_factory(name="Ren", entranced_channel_id=321)
    repo = character_repo_factory([target, active])

    with pytest.raises(AnotherCharacterIsActive):
        await EntranceUseCase(repo).execute(100, "Airi", 777)
