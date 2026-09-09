from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.character import Character


class AccoladeTeam(Base):
    __tablename__ = "accolade_teams"

    id: Mapped[int] = mapped_column(primary_key=True)

    accolade_result_id: Mapped[int] = mapped_column(
        ForeignKey("accolade_results.id"),
        unique=True,
        nullable=False,
    )

    act_id: Mapped[int | None] = mapped_column(
        ForeignKey("acts.id"),
        nullable=True,
    )

    members: Mapped[list["Character"]] = relationship(
        secondary="accolade_team_members",
        back_populates="accolade_teams",
    )