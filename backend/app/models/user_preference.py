from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.app.database.session import Base


class UserPreference(Base):
    """Reserved for future personalization and controller binding phase."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(128), unique=True, nullable=False, index=True)
    default_notation_mode = Column(String(16), nullable=False, default="ARROWS")  # ARROWS, ENGLISH, NUMPAD, CONTROLLER
    preferred_controller_layout = Column(String(16), nullable=False, default="PLAYSTATION")  # PLAYSTATION, XBOX, ARCADE
    favorite_character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    last_player_character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    last_opponent_character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    last_stage_id = Column(Integer, ForeignKey("stages.id"), nullable=True)
    last_conditions_json = Column(String(512), nullable=True)
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

