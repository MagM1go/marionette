import typing as t
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from marionette.domain.entities.base import Base
from marionette.domain.roles import Roles

if t.TYPE_CHECKING:
    from marionette.domain.entities.agency import Agency


class Character(Base):
    __tablename__: str = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger, index=True, nullable=False
    )
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
    agency: Mapped["Agency"] = relationship("Agency", back_populates="characters")
    home_channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    entranced_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    is_in_performance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    @property
    def age(self) -> int:
        today = datetime.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )
        
    @t.override
    def __repr__(self) -> str:
        return f"<Character(id={self.id}, user_id={self.user_id}, name='{self.name}', role={self.role}, is_active={self.is_active}, rating={self.rating})>"
