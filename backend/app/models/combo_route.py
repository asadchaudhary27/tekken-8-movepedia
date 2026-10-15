from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class ComboRoute(Base):
    """
    Verified Tekken 8 Combo Route Entity.
    Stores route notation, damage, difficulty, category (Midscreen, Wall Carry,
    Wall Combo, Wall Break, Floor Break, Balcony Break), and stage dependencies.
    Phase 5: Adds damage scaling calculations, launcher types, hurtbox compatibility,
    and easier execution alternatives.
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

    # Phase 5: Damage Scaling & Mechanics
    launcher_type = Column(String(64), nullable=False, default="NORMAL_HIT", index=True)  # NORMAL_HIT, COUNTER_HIT, WHILE_RISING, CROUCH, TORNADO_STARTER, STUN
    damage_type = Column(String(32), nullable=False, default="TESTED")  # TESTED, REPORTED, ESTIMATED, UNVERIFIED
    damage_calculation_method = Column(String(64), nullable=False, default="LAB_TESTED_IN_GAME")  # LAB_TESTED_IN_GAME, REPORTED_SOURCE, SCALED_ESTIMATE, UNVERIFIED
    raw_damage_sum = Column(Integer, nullable=True)  # Sum of unscaled hit damages (for scaling contrast)
    scaling_breakdown_json = Column(Text, nullable=True)  # Detailed hit-by-hit scaling list JSON

    # Execution & Stance
    execution_notes = Column(Text, nullable=True)
    required_stance = Column(String(64), nullable=True)  # e.g. ZEN, SENTAI, HEAVENS_WRATH, HUNTING, NONE

    # Hurtbox Profile Target
    target_hurtbox_class = Column(String(64), nullable=False, default="UNIVERSAL", index=True)  # UNIVERSAL, MALE_STANDARD, FEMALE_COMPACT, BIG, BEARS

    # Lower-Risk / Easier Execution Alternative
    easier_alternative_id = Column(Integer, ForeignKey("combo_routes.id"), nullable=True)
    easier_alternative_notes = Column(Text, nullable=True)

    verification_status = Column(String(32), nullable=False, default="VERIFIED")
    patch_version = Column(String(32), nullable=False, default="3.00.02")

    character = relationship("Character", back_populates="combos")
    starter_move = relationship("Move")
    stage = relationship("Stage")
    compatibilities = relationship("ComboCompatibility", back_populates="combo_route", cascade="all, delete-orphan")
    easier_alternative = relationship("ComboRoute", remote_side=[id])
