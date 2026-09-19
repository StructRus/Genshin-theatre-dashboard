from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String, CheckConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.run import Run
    from app.models.season_cast import SeasonCast


class TheatreSeason(Base):
    __tablename__ = "theatre_seasons"

    __table_args__ = (
        CheckConstraint(
            "cardinality(allowed_elements) = 3",
            name="ck_theatre_season_allowed_elements_count",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    season_number: Mapped[int] = mapped_column(nullable=False, unique=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    allowed_elements: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    runs: Mapped[list["Run"]] = relationship(back_populates="season")
    season_cast: Mapped["SeasonCast"] = relationship(back_populates="season")