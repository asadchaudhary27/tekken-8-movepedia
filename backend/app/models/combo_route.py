from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class ComboRoute(Base):
    __tablename__ = "combo_routes"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    starter_move_id = Column(Integer, ForeignKey("moves.id"), nullable=True)
    title = Column(String(128), nullable=False)
    notation_sequence = Column(Text, nullable=False)
    total_damage = Column(Integer, nullable=False, default=0)
    hit_count = Column(Integer, nullable=False, default=0)
    difficulty = Column(String(16), nullable=False, default="MEDIUM")  # EASY, MEDIUM, HARD, OPTIMAL
    uses_heat = Column(Boolean, nullable=False, default=False)
    uses_tornado = Column(Boolean, nullable=False, default=False)
    uses_wall = Column(Boolean, nullable=False, default=False)

    character = relationship("Character", back_populates="combos")
    starter_move = relationship("Move")
