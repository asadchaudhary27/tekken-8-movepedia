from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False, index=True)
    japanese_name = Column(String(128), nullable=True)
    archetype = Column(String(64), nullable=True, index=True)  # Mishima, Allies, Rebels, Newcomers, Grappler, etc.
    default_stance = Column(String(64), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    is_dlc = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    moves = relationship("Move", back_populates="character", cascade="all, delete-orphan")
    combos = relationship("ComboRoute", back_populates="character", cascade="all, delete-orphan")
