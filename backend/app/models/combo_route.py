from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class ComboRoute(Base):
    """
    Verified Tekken 8 Combo Route Entity.
    Stores route notation, damage, difficulty, category (Midscreen, Wall Carry,
    Wall Combo, Wall Break, Floor Break, Balcony Break), and stage dependencies.
    """
    __tablename__ = "combo_routes"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    starter_move_id = Column(Integer, ForeignKey("moves.id"), nullable=True)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=True, index=True)

    title = Column(String(128), nullable=False)
    notation_sequence = Column(Text, nullable=False)
    total_damage = Column(Integer, nullable=False, default=0)
    hit_count = Column(Integer, nullable=False, default=0)
    difficulty = Column(String(16), nullable=False, default="MEDIUM")  # EASY, MEDIUM, HARD, OPTIMAL

    # Tactical category: MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK
    combo_type = Column(String(32), nullable=False, default="MIDSCREEN", index=True)

    uses_heat = Column(Boolean, nullable=False, default=False)
    uses_tornado = Column(Boolean, nullable=False, default=False)
    uses_wall = Column(Boolean, nullable=False, default=False)
    requires_counter_hit = Column(Boolean, nullable=False, default=False)
    is_stage_dependent = Column(Boolean, nullable=False, default=False)

    stage_section = Column(String(64), nullable=True)
    starter_move_name = Column(String(128), nullable=True)
    starter_move_input = Column(String(64), nullable=True)
    ender_move_name = Column(String(128), nullable=True)
    ender_move_input = Column(String(64), nullable=True)
    conditions_notes = Column(Text, nullable=True)
    source = Column(String(128), nullable=False, default="TekkenDocs / Community Verified Lab")

    character = relationship("Character", back_populates="combos")
    starter_move = relationship("Move")
    stage = relationship("Stage")
