from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


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