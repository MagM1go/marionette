from collections.abc import Callable

import pytest

from marionette.application.usecases.exit_usecase import ExitLocationUseCase
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import (
    CharacterNotFound,
    CharacterNotInLocation,
    WrongChannel,
)
from tests.fakes import FakeCharacterRepository, FakeTransaction


@pytest.mark.asyncio
async def test_exit_clears_location_on_success(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(entranced_channel_id=777)
    repo = character_repo_factory([character])

    result = await ExitLocationUseCase(repo, fake_transaction).exit(100, "Airi", 777)

    assert result.location_id == 777
    assert character.entranced_channel_id is None
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_exit_raises_when_character_missing(
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    repo = character_repo_factory()

    with pytest.raises(CharacterNotFound):
        await ExitLocationUseCase(repo, fake_transaction).exit(100, "Airi", 777)

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_exit_raises_when_character_not_entranced(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    repo = character_repo_factory([character_factory()])

    with pytest.raises(CharacterNotInLocation):
        await ExitLocationUseCase(repo, fake_transaction).exit(100, "Airi", 777)

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_exit_raises_when_trying_to_exit_wrong_channel(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    repo = character_repo_factory([character_factory(entranced_channel_id=321)])

    with pytest.raises(WrongChannel):
        await ExitLocationUseCase(repo, fake_transaction).exit(100, "Airi", 777)

    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
