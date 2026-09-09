from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.theatre_season import TheatreSeason
    from app.models.character import Character


class SeasonCast(Base):
    __tablename__ = "season_casts"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("theatre_seasons.id"),
        nullable=False,
        unique=True,
    )

    season: Mapped["TheatreSeason"] = relationship(back_populates="season_cast")
    characters: Mapped[list["Character"]] = relationship(
        secondary="season_cast_members",
        back_populates="season_casts",
    )