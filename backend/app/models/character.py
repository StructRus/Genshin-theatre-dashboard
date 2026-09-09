from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.act import Act
    from app.models.season_cast import SeasonCast
    from app.models.run_cast import RunCast
    from app.models.accolade_team import AccoladeTeam


class Character(Base):

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    element: Mapped[str] = mapped_column(String(10), nullable=False)
    weapon_type: Mapped[str] = mapped_column(String(20), nullable=False)
    rarity: Mapped[int] = mapped_column(nullable=False)
    portrait_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    acts: Mapped[list["Act"]] = relationship(
        secondary="act_characters",
        back_populates="characters"
    )
    season_casts: Mapped[list["SeasonCast"]] = relationship(
        secondary="season_cast_members",
        back_populates="characters",
    )
    run_casts: Mapped[list["RunCast"]] = relationship(
        secondary="run_cast_members",
        back_populates="characters",
    )
    accolade_teams: Mapped[list["AccoladeTeam"]] = relationship(
        secondary="accolade_team_members",
        back_populates="members",
    )