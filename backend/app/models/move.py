from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    stable_source_id = Column(String(128), nullable=True, index=True)
    name = Column(String(128), nullable=True)
    original_notation = Column(String(128), nullable=False, index=True)
    normalized_notation = Column(String(128), nullable=False, index=True)

    # Core Frame & Gameplay Properties (Nullable to avoid treating unknown as zero)
    startup_frames = Column(Integer, nullable=True)
    startup_raw = Column(String(32), nullable=True)
    block_advantage = Column(Integer, nullable=True)
    block_advantage_raw = Column(String(32), nullable=True)
    hit_advantage = Column(Integer, nullable=True)
    hit_advantage_raw = Column(String(32), nullable=True)
    ch_advantage = Column(Integer, nullable=True)
    ch_advantage_raw = Column(String(32), nullable=True)
    damage = Column(Integer, nullable=True)
    damage_raw = Column(String(32), nullable=True)
    hit_level = Column(String(32), nullable=True)
    stance_context = Column(String(64), nullable=True)

    # Provenance and Quality
    patch_id = Column(Integer, ForeignKey("game_patches.id"), nullable=True, index=True)
    import_batch_id = Column(Integer, ForeignKey("import_batches.id"), nullable=True, index=True)
    verification_status = Column(String(32), nullable=False, default="UNVERIFIED")  # VERIFIED, UNVERIFIED, CONFLICTING
    verification_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("character_id", "normalized_notation", name="uq_char_move_notation"),
    )

    character = relationship("Character", back_populates="moves")
    patch = relationship("GamePatch", back_populates="moves")
    import_batch = relationship("ImportBatch", back_populates="moves")
    inputs = relationship("MoveInput", back_populates="move", cascade="all, delete-orphan", order_by="MoveInput.sequence_index")
    properties = relationship("MoveProperty", back_populates="move", cascade="all, delete-orphan")
    verification_records = relationship("VerificationRecord", back_populates="move", cascade="all, delete-orphan")
    conflicts = relationship("DataConflict", back_populates="move", cascade="all, delete-orphan")
    missing_issues = relationship("MissingDataIssue", back_populates="move", cascade="all, delete-orphan")


class MoveInput(Base):
    __tablename__ = "move_inputs"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=False, index=True)
    sequence_index = Column(Integer, nullable=False)
    direction_code = Column(String(8), nullable=False)  # u, ub, b, db, d, df, f, uf, n
    buttons_raw = Column(String(16), nullable=False)    # 1, 2, 1+2, etc.
    is_simultaneous = Column(Boolean, nullable=False, default=False)
    is_hold = Column(Boolean, nullable=False, default=False)
    is_just_frame = Column(Boolean, nullable=False, default=False)
    stance_name = Column(String(32), nullable=True)

    move = relationship("Move", back_populates="inputs")
