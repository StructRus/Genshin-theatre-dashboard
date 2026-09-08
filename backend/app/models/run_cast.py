from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RunCast(Base):
    __tablename__ = "run_casts"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id"),
        unique=True,
        nullable=False,
    )