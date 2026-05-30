from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import BigInteger

from marionette.domain.entities.base import Base
from marionette.domain.entities.subscription import Subscription


class Follower(Base):
    __tablename__ = "followers"

    id: Mapped[int] = mapped_column(primary_key=True)
    """ID фолловера"""

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    """ID пользователя, кому принадлежит отслеживаемый персонаж"""

    following: Mapped[list[Subscription]] = relationship(cascade="all, delete-orphan")
    """Это список подписок"""
