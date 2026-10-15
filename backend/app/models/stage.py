from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Stage(Base):
    """
    Verified Tekken 8 Battleground / Stage Entity.
    Stores boundary configuration, destructible hazards, transitions, and notes.
    """
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    location = Column(String(128), nullable=True)
    image_url = Column(String(256), nullable=False)

    # Boundary configuration
    has_walls = Column(Boolean, nullable=False, default=True)
    boundary_shape = Column(String(64), nullable=True)  # Octagonal, Rectangular, Square, Irregular

    # Wall mechanics
    wall_break = Column(Boolean, nullable=False, default=False)
    hard_wall_break = Column(Boolean, nullable=False, default=False)
    wall_blast = Column(Boolean, nullable=False, default=False)
    wall_bound = Column(Boolean, nullable=False, default=False)

    # Floor mechanics
    floor_break = Column(Boolean, nullable=False, default=False)
    floor_blast = Column(Boolean, nullable=False, default=False)

    # Balcony mechanics
    balcony_break = Column(Boolean, nullable=False, default=False)

    # Transitions & Sections
    has_transitions = Column(Boolean, nullable=False, default=False)
    transition_description = Column(Text, nullable=True)
    total_sections = Column(Integer, nullable=False, default=1)

    # Gimmicks, notes, and provenance
    special_mechanics = Column(String(256), nullable=True)
    notes = Column(Text, nullable=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True)

    data_source = relationship("DataSource")
