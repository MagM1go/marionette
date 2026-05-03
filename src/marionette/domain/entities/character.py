import typing as t
from datetime import UTC, datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CheckConstraint, ForeignKey

from marionette.domain.entities.base import Base
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from marionette.domain.roles import AgencyRoles, Roles
from marionette.domain.statuses import CharacterStatus

if t.TYPE_CHECKING:
    from marionette.domain.entities.agency import Agency


class Character(Base):
    __tablename__: str = "characters"
    __table_args__ = (
        CheckConstraint(
            "(agency_role IS NULL) = (agency_id IS NULL)",
            name="agency_role_requires_agency",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    """Означает, что персонаж находится в локации и выбран именно он, как персонаж, за которого игрок пишет"""

    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[Roles | None] = mapped_column()
    agency_role: Mapped[AgencyRoles | None] = mapped_column()
    biography: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column(default=0)
    birthday: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    agency_id: Mapped[int | None] = mapped_column(ForeignKey("agencies.id"))
    agency: Mapped[Agency] = relationship("Agency", back_populates="characters")
    entered_channel_id: Mapped[int | None] = mapped_column(BigInteger)
    is_in_performance: Mapped[bool] = mapped_column(Boolean, default=False)
    last_exposed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[CharacterStatus] = mapped_column(default=CharacterStatus.MODERATION)

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

    def abandon(self) -> None:
        if self.status == CharacterStatus.MODERATION or self.status == CharacterStatus.ABANDONED:
            raise ValueError(
                "Cannot abandon a character that has not passed moderation or is already abandoned."
            )

        self.status = CharacterStatus.ABANDONED

    def can_be_exposed(self, current_time: datetime) -> bool:
        if not self.last_exposed_at:
            return True

        last_exposed = self.last_exposed_at
        if last_exposed.tzinfo is None:
            last_exposed = last_exposed.replace(tzinfo=UTC)

        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=UTC)

        delta = current_time - last_exposed
        return delta.total_seconds() >= PaparazziPolicy.ONE_DAY

    def expose_to_paparazzi(self, new_rating: int, exposed_at: datetime) -> int:
        loss = self.rating - new_rating
        self.rating = new_rating
        self.last_exposed_at = exposed_at

        return loss

    def set_active(self, is_active: bool) -> None:
        self.is_active = is_active

    def set_location(self, location_id: int | None) -> None:
        self.entered_channel_id = location_id
