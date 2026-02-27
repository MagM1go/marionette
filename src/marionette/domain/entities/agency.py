# pyright: reportImportCycles=false
# базедпурайт говорит циклический импорт :muscle:
import typing as t

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger, Integer, String

from marionette.domain.entities.base import Base

if t.TYPE_CHECKING:
    from marionette.domain.entities.character import Character


class Agency(Base):
    __tablename__: str = "agencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    characters: Mapped[list["Character"]] = relationship(back_populates="agency")

    @t.override
    def __repr__(self) -> str:
        return f"Agency(id={self.id}, owner_id={self.owner_id}, name={self.name}, rating={self.rating})"
