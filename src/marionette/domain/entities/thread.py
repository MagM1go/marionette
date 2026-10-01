from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped

from marionette.domain.entities.base import Base


class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_paparazzi_trigger: Mapped[bool] = mapped_column(default=False)
