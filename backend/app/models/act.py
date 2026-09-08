from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Act(Base):
    __tablename__ = "acts"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id"),
        nullable=False,
    )

    act_number: Mapped[int] = mapped_column(nullable=False,)
    type: Mapped[str] = mapped_column(String(30), nullable=False,)

    #composite uniqueness : multiple runs can have same act
    __table_args__ = (UniqueConstraint("run_id", "act_number"),)