from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.character import Character


class RunCast(Base):
    __tablename__ = "run_casts"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id"),
        unique=True,
        nullable=False,
    )

    characters: Mapped[list["Character"]] = relationship(
        secondary="run_cast_members",
        back_populates="run_casts",
    )