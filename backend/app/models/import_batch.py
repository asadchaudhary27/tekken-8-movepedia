from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class ImportBatch(Base):
    __tablename__ = "import_batches"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False, index=True)
    source_url = Column(String(255), nullable=False)
    patch_version = Column(String(32), nullable=False, default="unknown")
    status = Column(String(32), nullable=False, default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED, FAILED, PARTIAL
    total_records = Column(Integer, nullable=False, default=0)
    successful_records = Column(Integer, nullable=False, default=0)
    failed_records = Column(Integer, nullable=False, default=0)
    raw_payload_path = Column(String(255), nullable=True)
    started_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    source = relationship("DataSource", back_populates="import_batches")
    moves = relationship("Move", back_populates="import_batch")
