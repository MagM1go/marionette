from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.types import BigInteger

from marionette.domain.entities.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    issuer_id: Mapped[int] = mapped_column(BigInteger())
    """Discord ID того, кто пожаловался"""

    reported_id: Mapped[int] = mapped_column(BigInteger())
    """Discord ID того, на кого пожаловались"""

    reason: Mapped[str] = mapped_column()
    """Причина жалобы"""
