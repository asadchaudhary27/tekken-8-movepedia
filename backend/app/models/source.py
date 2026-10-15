from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    base_url = Column(String(255), nullable=False)
    license_type = Column(String(64), nullable=False)
    approval_status = Column(String(32), nullable=False, default="RESEARCH_ONLY")
    rate_limit_policy = Column(String(128), nullable=False, default="1 request / sec")
    attribution_text = Column(Text, nullable=True)
    license_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    import_batches = relationship("ImportBatch", back_populates="source", cascade="all, delete-orphan")
