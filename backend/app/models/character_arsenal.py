"""
SQLAlchemy models for Character Arsenal extensions:
- CharacterThrow (Throws, command grabs, side/back throws)
- CharacterWallCombo (Max damage, post-tornado, and oki wall enders)
- CharacterTenHit (10-hit string counters, sequence breakdowns, and punish timings)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class CharacterThrow(Base):
    __tablename__ = "character_throws"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    character_name = Column(String(100), nullable=False)
    character_slug = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # Command Throw, Generic Throw, Side Throw, Back Throw
    throw_name = Column(String(120), nullable=False)
    command_input = Column(String(80), nullable=False)
    startup_frames = Column(String(30), nullable=False, default="i12")
    break_input = Column(String(40), nullable=False)
    break_window = Column(String(40), nullable=False, default="20f standard")
    visual_cue = Column(String(255), nullable=False)
    visual_cue_en = Column(String(255), nullable=True)
    visual_cue_ur = Column(String(255), nullable=True)
    damage = Column(String(30), nullable=False, default="35")
    damage_num = Column(Integer, nullable=False, default=35)
    oki_property = Column(String(255), nullable=True)
    oki_property_en = Column(String(255), nullable=True)
    oki_property_ur = Column(String(255), nullable=True)
    properties_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", backref="throws")


class CharacterWallCombo(Base):
    __tablename__ = "character_wall_combos"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    character_name = Column(String(100), nullable=False)
    character_slug = Column(String(100), nullable=False, index=True)
    route_type = Column(String(80), nullable=False)  # Max Damage Wall Combo, Post-Tornado Wall Ender, Oki / Setup
    combo_notation = Column(String(150), nullable=False)
    total_wall_damage = Column(String(40), nullable=False)
    damage_num = Column(Integer, nullable=False, default=35)
    spike_flip_property = Column(String(100), nullable=False)
    tactical_utility_notes = Column(Text, nullable=False)
    tactical_utility_notes_en = Column(Text, nullable=True)
    tactical_utility_notes_ur = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", backref="wall_combos")


class CharacterTenHit(Base):
    __tablename__ = "character_ten_hits"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    character_name = Column(String(100), nullable=False)
    character_slug = Column(String(100), nullable=False, index=True)
    combo_name = Column(String(120), nullable=False)
    combo_input = Column(String(120), nullable=False)
    hit_sequence_breakdown = Column(String(100), nullable=False)
    low_parry_duck_window = Column(String(255), nullable=False)
    low_parry_duck_window_en = Column(String(255), nullable=True)
    low_parry_duck_window_ur = Column(String(255), nullable=True)
    interrupt_gap = Column(String(255), nullable=False)
    interrupt_gap_en = Column(String(255), nullable=True)
    interrupt_gap_ur = Column(String(255), nullable=True)
    optimal_punish = Column(String(255), nullable=False)
    optimal_punish_en = Column(String(255), nullable=True)
    optimal_punish_ur = Column(String(255), nullable=True)
    how_to_counter = Column(Text, nullable=False)
    how_to_counter_en = Column(Text, nullable=True)
    how_to_counter_ur = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", backref="ten_hits")


class CharacterHeatSmash(Base):
    __tablename__ = "character_heat_smashes"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    character_name = Column(String(100), nullable=False)
    character_slug = Column(String(100), nullable=False, index=True)
    command_input = Column(String(80), nullable=False)
    startup_frames = Column(String(30), nullable=False)
    hit_level = Column(String(40), nullable=False)
    damage = Column(String(30), nullable=False)
    block_frames = Column(String(30), nullable=False)
    category = Column(String(100), nullable=False)
    stance_transition = Column(String(100), nullable=True)
    hazard_property = Column(String(100), nullable=True)
    properties_notes = Column(Text, nullable=True)
    properties_notes_en = Column(Text, nullable=True)
    properties_notes_ur = Column(Text, nullable=True)
    tactical_counter = Column(Text, nullable=True)
    tactical_counter_en = Column(Text, nullable=True)
    tactical_counter_ur = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    character = relationship("Character", backref="heat_smashes")


class MovementTechnique(Base):
    __tablename__ = "movement_techniques"

    id = Column(Integer, primary_key=True, index=True)
    technique_name = Column(String(120), nullable=False)
    technique_slug = Column(String(100), nullable=False, index=True)
    command_input = Column(String(100), nullable=False)
    socd_shortcut = Column(String(120), nullable=True)
    why_it_matters = Column(Text, nullable=False)
    why_it_matters_en = Column(Text, nullable=True)
    why_it_matters_ur = Column(Text, nullable=True)
    execution_breakdown = Column(Text, nullable=False)
    execution_breakdown_en = Column(Text, nullable=True)
    execution_breakdown_ur = Column(Text, nullable=True)
    tactical_application = Column(Text, nullable=False)
    tactical_application_en = Column(Text, nullable=True)
    tactical_application_ur = Column(Text, nullable=True)
    warning = Column(Text, nullable=True)
    warning_en = Column(Text, nullable=True)
    warning_ur = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class BlenderScenario(Base):
    __tablename__ = "blender_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String(100), nullable=False)
    character_slug = Column(String(100), nullable=False, index=True)
    scenario_title = Column(String(150), nullable=False)
    scenario_title_en = Column(String(150), nullable=True)
    scenario_title_ur = Column(String(150), nullable=True)
    frame_situation = Column(String(120), nullable=False)
    frame_situation_en = Column(String(120), nullable=True)
    frame_situation_ur = Column(String(120), nullable=True)
    panic_trigger = Column(Text, nullable=False)
    panic_trigger_en = Column(Text, nullable=True)
    panic_trigger_ur = Column(Text, nullable=True)
    verified_safe_response = Column(Text, nullable=False)
    verified_safe_response_en = Column(Text, nullable=True)
    verified_safe_response_ur = Column(Text, nullable=True)
    risk_reward_rating = Column(String(100), nullable=False)
    risk_reward_rating_en = Column(String(100), nullable=True)
    risk_reward_rating_ur = Column(String(100), nullable=True)
    practice_drill_input = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
