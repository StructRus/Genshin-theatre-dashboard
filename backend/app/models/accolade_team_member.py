from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AccoladeTeamMember(Base):
    __tablename__ = "accolade_team_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(
        ForeignKey("accolade_teams.id"),
        nullable=False,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "character_id",
            name="uq_accolade_team_member_character",
        ),
    )