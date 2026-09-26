from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RunCastMember(Base):
    __tablename__ = "run_cast_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_cast_id: Mapped[int] = mapped_column(
        ForeignKey("run_casts.id"),
        nullable=False,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        nullable=False,
    )

    cast_type: Mapped[str] = mapped_column(String(20), nullable=False,)
    trial: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False,)

    __table_args__ = (
        UniqueConstraint(
            "run_cast_id",
            "character_id",
            name="uq_run_cast_member_character",
        ),
    )