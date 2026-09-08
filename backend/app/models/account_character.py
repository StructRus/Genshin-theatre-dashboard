from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AccountCharacter(Base):
    __tablename__ = "account_characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        unique = True,
        nullable=False,
    )

    joining_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )