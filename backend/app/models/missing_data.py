from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class MissingDataIssue(Base):
    __tablename__ = "missing_data_issues"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=False, index=True)
    field_name = Column(String(32), nullable=False)
    reason_category = Column(String(32), nullable=False)  # NOT_PROVIDED, UNTESTED, INAPPLICABLE
    priority = Column(String(16), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    reported_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    move = relationship("Move", back_populates="missing_issues")
