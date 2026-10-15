from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Stage(Base):
    """
    Verified Tekken 8 Battleground / Stage Entity.
    Stores boundary configuration, destructible hazards, transitions,
    wall positions, geometric layout parameters, and tactical notes.
    """
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    location = Column(String(128), nullable=True)
    image_url = Column(String(256), nullable=False)

    # Boundary configuration
    has_walls = Column(Boolean, nullable=False, default=True)
    boundary_shape = Column(String(64), nullable=True)  # Octagonal, Rectangular, Square, Irregular, Infinite
    wall_distance = Column(String(64), nullable=True)   # e.g. "Standard (24m)", "Wide (32m)", "Narrow (18m)", "None (Infinite)"
    layout_description = Column(Text, nullable=True)

    # Wall mechanics
    wall_break = Column(Boolean, nullable=False, default=False)
    hard_wall_break = Column(Boolean, nullable=False, default=False)
    wall_blast = Column(Boolean, nullable=False, default=False)
    wall_bound = Column(Boolean, nullable=False, default=False)
    wall_break_interaction = Column(Text, nullable=True)

    # Floor mechanics
    floor_break = Column(Boolean, nullable=False, default=False)
    floor_blast = Column(Boolean, nullable=False, default=False)
    floor_break_interaction = Column(Text, nullable=True)

    # Balcony mechanics
    balcony_break = Column(Boolean, nullable=False, default=False)
    balcony_break_interaction = Column(Text, nullable=True)

    # Transitions & Sections
    has_transitions = Column(Boolean, nullable=False, default=False)
    transition_description = Column(Text, nullable=True)
    transition_conditions = Column(Text, nullable=True)
    total_sections = Column(Integer, nullable=False, default=1)

    # Tactical geometry data for SVG blueprint / map (null if unmapped or infinite)
    geometry_data_json = Column(Text, nullable=True)

    # Gimmicks, notes, and provenance
    special_mechanics = Column(String(256), nullable=True)
    notes = Column(Text, nullable=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True)

    data_source = relationship("DataSource")
