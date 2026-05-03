from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.types import BigInteger, DateTime

from marionette.domain.entities.base import Base


class Vote(Base):
    __tablename__: str = "votes"
    __table_args__ = (PrimaryKeyConstraint("character_id", "voted_by"),)

    character_id: Mapped[int] = mapped_column()
    """Персонаж, за которого проголосовали"""

    voted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    """Время, когда был отдан голос"""

    voted_by: Mapped[int] = mapped_column(BigInteger)
    """Кто именно проголосовал"""
