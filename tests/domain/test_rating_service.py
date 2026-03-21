from unittest.mock import patch

from marionette.domain.services.rating_service import (
    AgencyLevel,
    RatingChangeReason,
    RatingService,
    can_join_agency,
    get_agency_level,
    get_rating_divisor,
)


def test_get_rating_divisor_uses_expected_thresholds() -> None:
    assert get_rating_divisor(0) == 1.0
    assert get_rating_divisor(99) == 1.0
    assert get_rating_divisor(100) == 1.2
    assert get_rating_divisor(300) == 1.5
    assert get_rating_divisor(500) == 2.0
    assert get_rating_divisor(700) == 2.5
    assert get_rating_divisor(900) == 3.0
    assert get_rating_divisor(1000) == 4.0


def test_get_agency_level_uses_rating_boundaries() -> None:
    assert get_agency_level(0) == AgencyLevel.D
    assert get_agency_level(199) == AgencyLevel.D
    assert get_agency_level(200) == AgencyLevel.B
    assert get_agency_level(499) == AgencyLevel.B
    assert get_agency_level(500) == AgencyLevel.A
    assert get_agency_level(899) == AgencyLevel.A
    assert get_agency_level(900) == AgencyLevel.S


def test_can_join_agency_requires_minimum_rating() -> None:
    assert can_join_agency(200, AgencyLevel.B) is True
    assert can_join_agency(199, AgencyLevel.B) is False


@patch("marionette.domain.services.rating_service.random.randint", return_value=20)
def test_inc_character_rating_applies_divisor_and_agency_bonus(_: object) -> None:
    new_rating = RatingService().inc_character_rating(
        rating=300,
        reason=RatingChangeReason.PERFORMANCE,
        in_agency=True,
    )

    assert new_rating == 314


@patch("marionette.domain.services.rating_service.random.randint", return_value=30)
def test_dec_agency_rating_applies_divisor_and_level_penalty(_: object) -> None:
    new_rating = RatingService().dec_agency_rating(
        rating=500,
        reason=RatingChangeReason.SCANDAL,
    )

    assert new_rating == 422


def test_agency_cannot_use_performance_reason() -> None:
    service = RatingService()

    try:
        service.inc_agency_rating(100, RatingChangeReason.PERFORMANCE)
    except ValueError as error:
        assert str(error) == "PERFORMANCE недоступна для агентств"
    else:
        raise AssertionError("Expected ValueError for PERFORMANCE agency rating change")


def test_dec_agency_rating_from_member_scales_loss() -> None:
    new_rating = RatingService().dec_agency_rating_from_member(
        agency_rating=500,
        character_loss=35,
    )

    assert new_rating == 486
