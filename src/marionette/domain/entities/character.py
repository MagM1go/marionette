from __future__ import annotations

import typing as t
from datetime import UTC, datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from marionette.domain.entities.base import Base
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from marionette.domain.roles import Roles
from marionette.domain.services.rating_service import RatingChangeReason, RatingService

if t.TYPE_CHECKING:
    from marionette.domain.entities.agency import Agency


class Character(Base):
    __tablename__: str = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    agency_id: Mapped[int | None] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    agency: Mapped[Agency] = relationship("Agency", back_populates="characters")
    home_channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    entranced_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    is_in_performance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_exposed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    @t.override
    def __repr__(self) -> str:
        return (
            f"<Character(id={self.id}, user_id={self.user_id}, "
            f"name='{self.name}', role={self.role}, "
            f"is_active={self.is_active}, rating={self.rating})>"
        )

    @property
    def age(self) -> int:
        today = datetime.now(UTC)
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    def can_be_exposed(self) -> bool:
        if not self.last_exposed_at:
            return True

        delta = datetime.now(self.last_exposed_at.tzinfo) - self.last_exposed_at
        return delta.total_seconds() >= PaparazziPolicy.ONE_DAY

    def apply_paparazzi_incident(self, new_rating: int) -> None:
        self.rating = new_rating
        self.last_exposed_at = datetime.now(UTC)

    def expose_to_paparazzi(self, rating_service: RatingService) -> int:
        new_rating = rating_service.dec_character_rating(
            rating=self.rating, reason=RatingChangeReason.NEWS_NEGATIVE
        )
        loss = self.rating - new_rating
        self.rating = new_rating

        return loss
