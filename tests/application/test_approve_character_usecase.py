from collections.abc import Callable

import pytest

from marionette.application.protocols.types import CharacterId
from marionette.application.usecases.moderation.approve_character_usecase import (
    ApproveCharacterUseCase,
)
from marionette.domain.entities.character import Character
from marionette.domain.exceptions import (
    CharacterAlreadyActive,
    CharacterIsAbandoned,
    CharacterNotFound,
)
from marionette.domain.statuses import CharacterStatus
from tests.fakes import FakeCharacterRepository, FakeTransaction


@pytest.mark.asyncio
async def test_approve_marks_character_active_and_returns_name(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(id=10, name="Airi", status=CharacterStatus.MODERATION)
    repo = character_repo_factory([character])

    result = await ApproveCharacterUseCase(
        transaction=fake_transaction,
        character_repo=repo,
    ).approve(CharacterId(10))

    assert result == "Airi"
    assert character.status == CharacterStatus.IS_ACTIVE
    assert fake_transaction.commit_calls == 1
    assert fake_transaction.rollback_calls == 0


@pytest.mark.asyncio
async def test_approve_raises_when_character_missing(
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    repo = character_repo_factory([])

    with pytest.raises(CharacterNotFound) as error:
        await ApproveCharacterUseCase(
            transaction=fake_transaction,
            character_repo=repo,
        ).approve(CharacterId(42))

    assert error.value.name == "42"
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_approve_raises_when_character_already_active(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(id=10, status=CharacterStatus.IS_ACTIVE)
    repo = character_repo_factory([character])

    with pytest.raises(CharacterAlreadyActive):
        await ApproveCharacterUseCase(
            transaction=fake_transaction,
            character_repo=repo,
        ).approve(CharacterId(10))

    assert character.status == CharacterStatus.IS_ACTIVE
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1


@pytest.mark.asyncio
async def test_approve_raises_when_character_abandoned(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[[list[Character] | None], FakeCharacterRepository],
    fake_transaction: FakeTransaction,
) -> None:
    character = character_factory(id=10, status=CharacterStatus.ABANDONED)
    repo = character_repo_factory([character])

    with pytest.raises(CharacterIsAbandoned):
        await ApproveCharacterUseCase(
            transaction=fake_transaction,
            character_repo=repo,
        ).approve(CharacterId(10))

    assert character.status == CharacterStatus.ABANDONED
    assert fake_transaction.commit_calls == 0
    assert fake_transaction.rollback_calls == 1
