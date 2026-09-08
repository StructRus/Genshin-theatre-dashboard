from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("theatre_seasons.id"),
        nullable=False,
    )
    
    time_elapsed_seconds: Mapped[int] = mapped_column(nullable=False,)
    fantasia_flowers_used: Mapped[int] = mapped_column(nullable=False,)
    total_characters_appeared: Mapped[int] = mapped_column(nullable=False,)
    stars_earned: Mapped[int] = mapped_column(nullable=False,)