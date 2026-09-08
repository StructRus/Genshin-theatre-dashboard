from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ActCharacter(Base):
    __tablename__ = "act_characters"

    #composite primary key : act_id + character_id
    act_id: Mapped[int] = mapped_column(
        ForeignKey("acts.id"),
        primary_key=True,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        primary_key=True,
    )