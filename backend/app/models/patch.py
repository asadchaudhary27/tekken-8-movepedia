from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class GamePatch(Base):
    __tablename__ = "game_patches"

    id = Column(Integer, primary_key=True, index=True)
    version_number = Column(String(32), unique=True, nullable=False, index=True)
    release_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    is_current = Column(Boolean, nullable=False, default=False)

    moves = relationship("Move", back_populates="patch")
