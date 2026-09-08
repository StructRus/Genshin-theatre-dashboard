from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Character(Base):

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    element: Mapped[str] = mapped_column(String(10), nullable=False)
    weapon_type: Mapped[str] = mapped_column(String(20), nullable=False)
    rarity: Mapped[int] = mapped_column(nullable=False)
    portrait_url: Mapped[str | None] = mapped_column(String(500), nullable=True)