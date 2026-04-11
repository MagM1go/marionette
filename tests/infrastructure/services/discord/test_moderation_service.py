from collections.abc import Mapping
from unittest.mock import AsyncMock, Mock, call

import hikari
import pytest

from marionette.bootstrap.config import config
from marionette.infrastructure.services.discord.moderation_service import HikariRoleplayModeration


@pytest.fixture
def rp_category_id(monkeypatch: pytest.MonkeyPatch) -> int:
    value = 100
    monkeypatch.setattr(config.discord, "rp_categories", [value])
    return value


def _make_channel(channel_type: type[object], *, channel_id: int, parent_id: int | None) -> Mock:
    return Mock(spec=channel_type, id=channel_id, parent_id=parent_id)


def _build_service(
    *,
    guild_channels: Mapping[int, object] | None = None,
    threads: Mapping[int, object] | None = None,
    fetched_channels: Mapping[int, object] | None = None,
    fetch_side_effect: BaseException | None = None,
) -> tuple[HikariRoleplayModeration, Mock, AsyncMock]:
    cache = Mock(spec=hikari.api.Cache)
    cache.get_guild_channel.side_effect = lambda channel_id: (guild_channels or {}).get(channel_id)
    cache.get_thread.side_effect = lambda channel_id: (threads or {}).get(channel_id)

    if fetch_side_effect is not None:
        fetch_channel = AsyncMock(side_effect=fetch_side_effect)
    else:
        fetch_channel = AsyncMock(
            side_effect=lambda channel_id: (
                fetched_channels[channel_id]
                if fetched_channels is not None and channel_id in fetched_channels
                else pytest.fail(f"unexpected fetch_channel({channel_id})")
            )
        )

    rest = Mock(spec=hikari.api.RESTClient)
    rest.fetch_channel = fetch_channel

    return HikariRoleplayModeration(cache, rest), cache, fetch_channel


@pytest.mark.asyncio
async def test_is_rp_location_returns_true_for_text_channel_from_cache(
    rp_category_id: int,
) -> None:
    category = _make_channel(hikari.GuildCategory, channel_id=rp_category_id, parent_id=None)
    channel = _make_channel(hikari.GuildTextChannel, channel_id=200, parent_id=rp_category_id)
    service, _, fetch_channel = _build_service(
        guild_channels={
            channel.id: channel,
            rp_category_id: category,
        }
    )

    assert await service.is_rp_location(channel.id) is True
    fetch_channel.assert_not_awaited()


@pytest.mark.asyncio
async def test_is_rp_location_returns_true_for_thread_from_cache_chain(
    rp_category_id: int,
) -> None:
    parent_channel_id = 200
    category = _make_channel(hikari.GuildCategory, channel_id=rp_category_id, parent_id=None)
    parent_channel = _make_channel(
        hikari.GuildTextChannel,
        channel_id=parent_channel_id,
        parent_id=rp_category_id,
    )
    thread = _make_channel(hikari.GuildThreadChannel, channel_id=300, parent_id=parent_channel_id)
    service, _, fetch_channel = _build_service(
        guild_channels={
            parent_channel_id: parent_channel,
            rp_category_id: category,
        },
        threads={thread.id: thread},
    )

    assert await service.is_rp_location(thread.id) is True
    fetch_channel.assert_not_awaited()


@pytest.mark.asyncio
async def test_is_rp_location_fetches_missing_parent_chain_from_rest(
    rp_category_id: int,
) -> None:
    parent_channel_id = 200
    category = _make_channel(hikari.GuildCategory, channel_id=rp_category_id, parent_id=None)
    parent_channel = _make_channel(
        hikari.GuildTextChannel,
        channel_id=parent_channel_id,
        parent_id=rp_category_id,
    )
    thread = _make_channel(hikari.GuildThreadChannel, channel_id=300, parent_id=parent_channel_id)
    service, cache, fetch_channel = _build_service(
        threads={thread.id: thread},
        fetched_channels={
            parent_channel_id: parent_channel,
            rp_category_id: category,
        },
    )

    assert await service.is_rp_location(thread.id) is True
    assert cache.get_guild_channel.call_args_list == [
        call(thread.id),
        call(parent_channel_id),
        call(rp_category_id),
    ]
    assert cache.get_thread.call_args_list == [
        call(thread.id),
        call(parent_channel_id),
        call(rp_category_id),
    ]
    assert fetch_channel.await_args_list == [call(parent_channel_id), call(rp_category_id)]


@pytest.mark.asyncio
async def test_is_rp_location_returns_false_for_non_rp_thread(
    rp_category_id: int,
) -> None:
    other_category_id = 101
    parent_channel_id = 200
    other_category = _make_channel(
        hikari.GuildCategory, channel_id=other_category_id, parent_id=None
    )
    parent_channel = _make_channel(
        hikari.GuildTextChannel,
        channel_id=parent_channel_id,
        parent_id=other_category_id,
    )
    thread = _make_channel(hikari.GuildThreadChannel, channel_id=300, parent_id=parent_channel_id)
    service, _, fetch_channel = _build_service(
        guild_channels={
            parent_channel_id: parent_channel,
            other_category_id: other_category,
        },
        threads={thread.id: thread},
    )

    assert await service.is_rp_location(thread.id) is False
    fetch_channel.assert_not_awaited()


@pytest.mark.asyncio
async def test_is_rp_location_returns_false_when_rest_cannot_fetch_parent(
    rp_category_id: int,
) -> None:
    thread = _make_channel(hikari.GuildThreadChannel, channel_id=300, parent_id=200)
    service, _, fetch_channel = _build_service(
        threads={thread.id: thread},
        fetch_side_effect=hikari.NotFoundError(
            url="/channels/200",
            headers={},
            raw_body=b"",
            message="not found",
            code=10003,
        ),
    )

    assert await service.is_rp_location(thread.id) is False
    fetch_channel.assert_awaited_once_with(200)
