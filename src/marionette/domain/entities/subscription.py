from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.functions import func
from sqlalchemy.types import BigInteger, DateTime

from marionette.domain.entities.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(BigInteger)
    character_author_id: Mapped[int] = mapped_column(BigInteger)
    character_id: Mapped[int] = mapped_column(BigInteger)
    followed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
