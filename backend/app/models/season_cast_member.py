from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SeasonCastMember(Base):
    __tablename__ = "season_cast_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_cast_id: Mapped[int] = mapped_column(
        ForeignKey("season_casts.id"),
        nullable=False,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        nullable=False,
    )

    cast_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )