from datetime import datetime
from enum import StrEnum

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.types import BigInteger, DateTime

from marionette.domain.entities.base import Base


class VoteSource(StrEnum):
    COMMAND = "command"
    REVIEW = "review"


class Vote(Base):
    __tablename__: str = "votes"
    __table_args__ = (
        UniqueConstraint("voted_by", "perfomance_id", name="uq_votes_voted_by_perfomance_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    character_id: Mapped[int] = mapped_column(index=True)
    """Персонаж, за которого проголосовали"""

    voted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    """Время, когда был отдан голос"""

    voted_by: Mapped[int] = mapped_column(BigInteger)
    """Кто последним проголосовал"""

    reputation: Mapped[int] = mapped_column(default=1)
    """То, сколько репутации даёт один голос"""

    source: Mapped[VoteSource] = mapped_column(default=VoteSource.COMMAND)
    """Источник голоса."""

    perfomance_id: Mapped[int | None] = mapped_column(BigInteger)
    """Публикация (выступление), за которую отдан голос. `None` для голосов из `/vote`."""
