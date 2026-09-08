from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TheatreSeason(Base):
    __tablename__ = "theatre_seasons"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_number: Mapped[int] = mapped_column(nullable=False, unique=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    allowed_elements: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)