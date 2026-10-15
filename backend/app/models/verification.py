from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class VerificationRecord(Base):
    """
    Non-destructive audit trail and provenance record.
    Tracks all changes, verifications, corrections, and import overrides across
    moves, combos, matchup notes, compatibility, stage mechanics, and punishes.
    """
    __tablename__ = "verification_records"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(32), nullable=False, default="MOVE", index=True)  # MOVE, COMBO, MATCHUP_NOTE, COMPATIBILITY, STAGE, PUNISH
    entity_id = Column(Integer, nullable=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=True, index=True)

    field_name = Column(String(64), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    verified_by = Column(String(64), nullable=False, default="System / Lab Team")
    method = Column(String(32), nullable=False, default="LAB_TEST")  # LAB_TEST, COMMUNITY_CONSENSUS, UPSTREAM_DIFF, MANUAL_EDIT, CSV_IMPORT
    result = Column(String(32), nullable=False, default="VERIFIED")  # VERIFIED, UNVERIFIED, CONFLICTING, UNAVAILABLE, CONFIRMED_ABSENT
    evidence_notes = Column(Text, nullable=True)
    change_summary = Column(Text, nullable=True)
    patch_version = Column(String(32), nullable=False, default="3.00.02")
    source_url = Column(String(255), nullable=True)
    verified_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    move = relationship("Move", back_populates="verification_records")
