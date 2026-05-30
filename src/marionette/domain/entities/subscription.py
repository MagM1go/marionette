from datetime import datetime

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.functions import func
from sqlalchemy.types import DateTime

from marionette.domain.entities.base import Base
from marionette.domain.entities.character import Character


class Subscription(Base):
    __tablename__ = "subscriptions"

    follower_id: Mapped[int] = mapped_column(ForeignKey("followers.id"), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), primary_key=True)
    followed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_defalt=func.now())
    character: Mapped[Character] = relationship()
