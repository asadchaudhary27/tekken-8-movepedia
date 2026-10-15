from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class PracticeRecord(Base):
    """
    Stores interactive practice mode attempts, mastery scores,
    and training checklist progress per session.
    """
    __tablename__ = "practice_records"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(128), nullable=False, index=True)
    player_character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    opponent_character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    opponent_move_id = Column(Integer, ForeignKey("moves.id"), nullable=True, index=True)
    opponent_move_name = Column(String(128), nullable=False)
    opponent_move_input = Column(String(128), nullable=False)
    punish_move_input = Column(String(128), nullable=False)

    success_count = Column(Integer, default=0, nullable=False)
    fail_count = Column(Integer, default=0, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    mastery_score = Column(Integer, default=0, nullable=False)  # 0 to 100
    last_practiced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = Column(Text, nullable=True)

    player_character = relationship("Character", foreign_keys=[player_character_id])
    opponent_character = relationship("Character", foreign_keys=[opponent_character_id])
    opponent_move = relationship("Move", foreign_keys=[opponent_move_id])
