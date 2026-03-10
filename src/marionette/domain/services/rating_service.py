import random
from enum import IntEnum, StrEnum


class RatingChangeReason(StrEnum):
    VOTE = "vote"
    PERFORMANCE = "performance"
    NEWS_POSITIVE = "news_positive"
    NEWS_NEGATIVE = "news_negative"
    SCANDAL = "scandal"
    SEASON_RESET = "season_reset"


class AgencyLevel(IntEnum):
    """
    | Уровень | Статус      | Минимальный рейтинг |
    | ------- | ----------- | ------------------- |
    | D       | Новички     | 0                   |
    | B       | Известные   | 200+                |
    | A       | Элита       | 500+                |
    | S       | Легендарные | 900+                |
    """

    D = 0
    B = 200
    A = 500
    S = 900


AGENCY_LEVEL_INFO = {
    AgencyLevel.D: {
        "name": "Новички",
        "description": "Начинающие агентства без требований к рейтингу",
    },
    AgencyLevel.B: {
        "name": "Известные",
        "description": "Агентства с хорошей репутацией",
    },
    AgencyLevel.A: {
        "name": "Элита",
        "description": "Топовые агентства с высокими стандартами",
    },
    AgencyLevel.S: {
        "name": "Легендарные",
        "description": "Элитные агентства с богатой историей",
    },
}

CHARACTER_ONLY_REASONS = {RatingChangeReason.PERFORMANCE}

REASON_WEIGHTS = {
    RatingChangeReason.VOTE: (2, 4),
    RatingChangeReason.PERFORMANCE: (15, 25),
    RatingChangeReason.NEWS_POSITIVE: (8, 15),
    RatingChangeReason.NEWS_NEGATIVE: (-12, -6),
    RatingChangeReason.SCANDAL: (-40, -25),
}

RATING_DIVISORS = [
    (100, 1.0),
    (300, 1.2),
    (500, 1.5),
    (700, 2.0),
    (900, 2.5),
    (1000, 3.0),
    (float("inf"), 4.0),
]

AGENCY_BONUS = 1.12

AGENCY_LEVEL_PENALTY = {
    AgencyLevel.D: 1.0,
    AgencyLevel.B: 1.15,
    AgencyLevel.A: 1.3,
    AgencyLevel.S: 1.5,
}


def get_rating_divisor(rating: int) -> float:
    """
    | Рейтинг | Делитель |
    | ------- | -------- |
    | 0-99    | ÷1.0     |
    | 100-299 | ÷1.2     |
    | 300-499 | ÷1.5     |
    | 500-699 | ÷2.0     |
    | 700-899 | ÷2.5     |
    | 900-999 | ÷3.0     |
    | 1000+   | ÷4.0     |
    """
    for threshold, divisor in RATING_DIVISORS:
        if rating < threshold:
            return divisor
    return 4.0


def get_agency_level(agency_rating: int) -> AgencyLevel:
    if agency_rating >= AgencyLevel.S:
        return AgencyLevel.S
    elif agency_rating >= AgencyLevel.A:
        return AgencyLevel.A
    elif agency_rating >= AgencyLevel.B:
        return AgencyLevel.B
    return AgencyLevel.D


def can_join_agency(character_rating: int, agency_level: AgencyLevel) -> bool:
    return character_rating >= agency_level


def get_agency_penalty(agency_level: AgencyLevel) -> float:
    return AGENCY_LEVEL_PENALTY[agency_level]


def is_reason_valid_for_agency(reason: RatingChangeReason) -> bool:
    return reason not in CHARACTER_ONLY_REASONS


class RatingService:
    """
    Сервис для управления рейтингом персонажей и агентств.

    - Новичкам легче расти, топам сложнее (делители)
    - Агентство даёт +12% к приросту, но больше потерь
    - PERFORMANCE доступна только персонажам
    """

    def _calculate_change(
        self,
        rating: int,
        weight_range: tuple[int, int],
        is_increase: bool,
        in_agency: bool = False,
        agency_penalty: float = 1.0,
    ) -> int:
        min_w, max_w = min(weight_range), max(weight_range)
        divisor = get_rating_divisor(rating)
        base = random.randint(min_w, max_w)

        if is_increase:
            change = base / divisor
            if in_agency:
                change *= AGENCY_BONUS
            return max(1, int(change))
        else:
            change = base * divisor * agency_penalty
            return -abs(int(change))

    def _validate_reason(
        self, reason: RatingChangeReason, for_agency: bool = False
    ) -> None:
        if reason not in REASON_WEIGHTS:
            raise ValueError(f"Неизвестная причина: {reason}")
        if for_agency and reason == RatingChangeReason.PERFORMANCE:
            raise ValueError("PERFORMANCE недоступна для агентств")

    def _scale_weights(
        self, reason: RatingChangeReason, n: int, invert: bool = False
    ) -> tuple[int, int]:
        min_w, max_w = REASON_WEIGHTS[reason]
        if invert and min_w < 0:
            return abs(max_w) * n, abs(min_w) * n
        return min_w * n, max_w * n

    def inc_character_rating(
        self,
        rating: int,
        reason: RatingChangeReason,
        n: int = 1,
        in_agency: bool = False,
    ) -> int:
        self._validate_reason(reason)
        scaled = self._scale_weights(reason, n, invert=True)
        change = self._calculate_change(
            rating, scaled, is_increase=True, in_agency=in_agency
        )
        return max(0, rating + change)

    def dec_character_rating(
        self, rating: int, reason: RatingChangeReason, n: int = 1
    ) -> int:
        self._validate_reason(reason)
        scaled = self._scale_weights(reason, n)
        change = self._calculate_change(rating, scaled, is_increase=False)
        return max(0, rating + change)

    def inc_agency_rating(
        self, rating: int, reason: RatingChangeReason, n: int = 1
    ) -> int:
        self._validate_reason(reason, for_agency=True)
        scaled = self._scale_weights(reason, n, invert=True)
        change = self._calculate_change(
            rating, scaled, is_increase=True, in_agency=True
        )
        return max(0, rating + change)

    def dec_agency_rating(
        self, rating: int, reason: RatingChangeReason, n: int = 1
    ) -> int:
        self._validate_reason(reason, for_agency=True)
        scaled = self._scale_weights(reason, n)
        penalty = get_agency_penalty(get_agency_level(rating))
        change = self._calculate_change(
            rating, scaled, is_increase=False, agency_penalty=penalty
        )
        return max(0, rating + change)

    def dec_agency_rating_from_member(
        self,
        agency_rating: int,
        character_loss: int,
        ratio: float = 0.4,
    ) -> int:
        penalty = int(abs(character_loss) * ratio)
        return max(0, agency_rating - penalty)
