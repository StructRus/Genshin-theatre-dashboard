from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.theatre_season import TheatreSeason


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("theatre_seasons.id"),
        nullable=False,
    )
    season: Mapped["TheatreSeason"] = relationship(back_populates="runs")

    time_elapsed_seconds: Mapped[int] = mapped_column(nullable=False,)
    fantasia_flowers_used: Mapped[int] = mapped_column(nullable=False,)
    total_characters_appeared: Mapped[int] = mapped_column(nullable=False,)
    stars_earned: Mapped[int] = mapped_column(nullable=False,)