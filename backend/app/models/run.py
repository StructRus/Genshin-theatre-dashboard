from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, CheckConstraint
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

    __table_args__ = (
        CheckConstraint(
            "time_elapsed_seconds >= 0",
            name="ck_run_time_elapsed_nonnegative",
        ),
        CheckConstraint(
            "fantasia_flowers_used >= 0",
            name="ck_run_fantasia_flowers_nonnegative",
        ),
        CheckConstraint(
            "total_characters_appeared >= 0",
            name="ck_run_total_characters_nonnegative",
        ),
        CheckConstraint(
            "stars_earned >= 0",
            name="ck_run_stars_nonnegative",
        ),
    )