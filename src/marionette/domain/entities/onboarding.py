from __future__ import annotations

from datetime import UTC, datetime
from enum import IntEnum
from typing import Any

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from marionette.domain.entities.base import Base


class OnboardingStep(IntEnum):
    NEWBIE = 0
    WELCOME = 1
    INTRO = 2
    RULES = 3
    REGISTRATION = 5
    COMPLETED = 6


class OnboardingState(Base):
    __tablename__ = "onboarding_states"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    current_step: Mapped[OnboardingStep] = mapped_column(
        Enum(OnboardingStep, native_enum=False),
        nullable=False,
        default=OnboardingStep.NEWBIE,
    )
    is_complete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def move_to_step(self, step: OnboardingStep) -> None:
        if self.is_complete:
            return
        self.current_step = step
        if step == OnboardingStep.COMPLETED:
            self.is_complete = True
            self.completed_at = datetime.now(UTC)


class OnboardingRoleGrant(Base):
    __tablename__ = "onboarding_role_grants"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class OnboardingEvent(Base):
    __tablename__ = "onboarding_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    step: Mapped[OnboardingStep | None] = mapped_column(
        Enum(OnboardingStep, native_enum=False),
        nullable=True,
    )
    payload: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
