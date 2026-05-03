from collections.abc import Callable

import pytest

from marionette.application.usecases.delete_offtopic_message_usecase import (
    DeleteOfftopicMessageUseCase,
)
from marionette.domain.entities.character import Character
from tests.fakes import FakeCharacterRepository


@pytest.mark.parametrize("message_content", [None, ""])
async def test_execute_returns_false_for_empty_message_content(
    character_repo_factory: Callable[..., FakeCharacterRepository],
    message_content: str | None,
) -> None:
    usecase = DeleteOfftopicMessageUseCase(character_repo_factory())

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content=message_content,
    )

    assert result is False


async def test_execute_returns_false_for_current_character_location_with_rp_message(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entered_channel_id=777)])
    usecase = DeleteOfftopicMessageUseCase(repo)

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="RP message",
    )

    assert result is False


async def test_execute_returns_false_for_current_character_location_with_non_rp_message(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entered_channel_id=777)])
    usecase = DeleteOfftopicMessageUseCase(repo)

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="// OOC message",
    )

    assert result is False


async def test_execute_returns_false_for_non_rp_message_from_another_location(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entered_channel_id=321)])
    usecase = DeleteOfftopicMessageUseCase(repo)

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="// OOC message",
    )

    assert result is False


async def test_execute_returns_true_for_rp_message_from_another_location(
    character_factory: Callable[..., Character],
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    repo = character_repo_factory([character_factory(entered_channel_id=321)])
    usecase = DeleteOfftopicMessageUseCase(repo)

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="RP message",
    )

    assert result is True


async def test_execute_returns_true_for_rp_message_when_character_is_not_entered(
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    usecase = DeleteOfftopicMessageUseCase(character_repo_factory())

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="RP message",
    )

    assert result is True


async def test_execute_returns_false_for_non_rp_message_when_character_is_not_entered(
    character_repo_factory: Callable[..., FakeCharacterRepository],
) -> None:
    usecase = DeleteOfftopicMessageUseCase(character_repo_factory())

    result = await usecase.execute(
        user_id=100,
        channel_id=777,
        message_content="// OOC message",
    )

    assert result is False
