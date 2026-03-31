from collections.abc import Callable

import pytest

from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import (
    CharacterNotFound,
    CharacterNotInLocation,
    WrongChannel,
)
from tests.fakes import FakeCharacterRepository, FakeUnitOfWork


@pytest.mark.asyncio
async def test_execute_clears_location_on_success(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_uow: FakeUnitOfWork,
) -> None:
    character = character_factory(entranced_channel_id=777)
    repo = character_repo_factory([character])

    result = await ExitUseCase(repo, fake_uow).execute(100, "Airi", 777)

    assert result.location_id == 777
    assert character.entranced_channel_id is None
    assert fake_uow.commit_calls == 1
    assert fake_uow.rollback_calls == 0


@pytest.mark.asyncio
async def test_execute_raises_when_character_missing(
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_uow: FakeUnitOfWork,
) -> None:
    repo = character_repo_factory()

    with pytest.raises(CharacterNotFound):
        await ExitUseCase(repo, fake_uow).execute(100, "Airi", 777)

    assert fake_uow.commit_calls == 0
    assert fake_uow.rollback_calls == 1


@pytest.mark.asyncio
async def test_execute_raises_when_character_not_entranced(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_uow: FakeUnitOfWork,
) -> None:
    repo = character_repo_factory([character_factory()])

    with pytest.raises(CharacterNotInLocation):
        await ExitUseCase(repo, fake_uow).execute(100, "Airi", 777)

    assert fake_uow.commit_calls == 0
    assert fake_uow.rollback_calls == 1


@pytest.mark.asyncio
async def test_execute_raises_when_trying_to_exit_wrong_channel(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
    fake_uow: FakeUnitOfWork,
) -> None:
    repo = character_repo_factory([character_factory(entranced_channel_id=321)])

    with pytest.raises(WrongChannel):
        await ExitUseCase(repo, fake_uow).execute(100, "Airi", 777)

    assert fake_uow.commit_calls == 0
    assert fake_uow.rollback_calls == 1
