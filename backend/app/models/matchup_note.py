from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class MatchupNote(Base):
    """
    Verified qualitative matchup notes between specific character pairings on a stage.
    """
    __tablename__ = "matchup_notes"

    id = Column(Integer, primary_key=True, index=True)
    player_character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    opponent_character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=True, index=True)

    overview = Column(Text, nullable=True)
    key_advice = Column(Text, nullable=True)
    strengths_vs_opponent = Column(Text, nullable=True)
    weaknesses_vs_opponent = Column(Text, nullable=True)

    # Phase 2 Intelligence & Provenance
    rating = Column(String(30), default="INSUFFICIENT_DATA", nullable=False)  # FAVORABLE, EVEN, UNFAVORABLE, INSUFFICIENT_DATA
    rating_reasoning = Column(Text, nullable=True)
    confidence_level = Column(String(20), default="NONE", nullable=False)  # HIGH, MEDIUM, LOW, NONE
    confidence_score = Column(Integer, default=0, nullable=False)  # 0 to 100

    player_strengths_json = Column(Text, nullable=True)
    opponent_strengths_json = Column(Text, nullable=True)
    useful_moves_json = Column(Text, nullable=True)
    dangerous_moves_json = Column(Text, nullable=True)

    spacing_and_movement = Column(Text, nullable=True)
    defensive_options = Column(Text, nullable=True)
    sidestep_and_tracking = Column(Text, nullable=True)
    heat_and_mechanics = Column(Text, nullable=True)
    stage_considerations = Column(Text, nullable=True)

    evidence_sources = Column(Text, nullable=True)
    unknown_or_unverified = Column(Text, nullable=True)
    patch_version = Column(String(30), default="3.00.02", nullable=False)
    contributor = Column(String(100), default="Tekken Lab Verification Team", nullable=True)
    verification_status = Column(String(50), default="VERIFIED", nullable=False)
    last_reviewed = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    player_character = relationship("Character", foreign_keys=[player_character_id])
    opponent_character = relationship("Character", foreign_keys=[opponent_character_id])
    stage = relationship("Stage")

