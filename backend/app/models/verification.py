from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=False, index=True)
    verified_by = Column(String(64), nullable=False)
    method = Column(String(32), nullable=False)  # LAB_TEST, COMMUNITY_CONSENSUS, UPSTREAM_DIFF
    result = Column(String(32), nullable=False)  # CONFIRMED, CORRECTED, DISPUTED
    evidence_notes = Column(Text, nullable=True)
    verified_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    move = relationship("Move", back_populates="verification_records")
