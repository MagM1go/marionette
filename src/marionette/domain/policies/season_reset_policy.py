import typing as t


class SeasonResetPolicy:
    THRESHOLDS: t.Final[t.Sequence[tuple[int, int]]] = [
        (100, 0),
        (300, 25),
        (500, 70),
        (700, 150),
        (900, 200),
        (1000, 300),
    ]
    DEFAULT_RESET_RATING: t.Final[int] = 400

    @classmethod
    def get_reset_rating(cls, rating: int) -> int:
        for max_value, bound in cls.THRESHOLDS:
            if rating < max_value:
                return bound

        return cls.DEFAULT_RESET_RATING
