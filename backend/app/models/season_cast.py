from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SeasonCast(Base):
    __tablename__ = "season_casts"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("theatre_seasons.id"),
        nullable=False,
        unique=True,
    )