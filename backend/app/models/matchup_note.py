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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    player_character = relationship("Character", foreign_keys=[player_character_id])
    opponent_character = relationship("Character", foreign_keys=[opponent_character_id])
    stage = relationship("Stage")
