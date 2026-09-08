from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AccoladeResult(Base):
    __tablename__ = "accolade_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id"),
        nullable=False,
    )

    accolade_id: Mapped[int] = mapped_column(
        ForeignKey("accolades.id"),
        nullable=False,
    )

    character_id: Mapped[int | None] = mapped_column(
        ForeignKey("characters.id"),
        nullable=True,
    )

    value: Mapped[int | None] = mapped_column(nullable=True,)