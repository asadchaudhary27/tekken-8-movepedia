from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class DataConflict(Base):
    __tablename__ = "data_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=False, index=True)
    field_name = Column(String(32), nullable=False)
    source_a_value = Column(String(64), nullable=False)
    source_b_value = Column(String(64), nullable=False)
    resolution_status = Column(String(32), nullable=False, default="UNRESOLVED")  # UNRESOLVED, RESOLVED, ESCALATED
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    move = relationship("Move", back_populates="conflicts")
