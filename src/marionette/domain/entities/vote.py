from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.types import BigInteger, DateTime

from marionette.domain.entities.base import Base


class Vote(Base):
    __tablename__: str = "votes"

    character_id: Mapped[int] = mapped_column(primary_key=True)
    """Персонаж, за которого проголосовали"""

    voted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    """Время, когда был отдан голос"""

    voted_by: Mapped[int] = mapped_column(BigInteger)
    """Кто последним проголосовал"""
