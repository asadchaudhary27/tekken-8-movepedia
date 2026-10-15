from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class ComboCompatibility(Base):
    """
    Phase 5: Opponent-Specific Juggle Compatibility Entity.
    Models character-specific and hurtbox-specific juggle interactions without
    assuming a single universal weight class.
    Tracks whether a combo connects reliably, requires timing adjustment,
    or drops on specific opponents.
    """
    __tablename__ = "combo_compatibilities"

    id = Column(Integer, primary_key=True, index=True)
    combo_route_id = Column(Integer, ForeignKey("combo_routes.id"), nullable=False, index=True)
    opponent_character_id = Column(Integer, ForeignKey("characters.id"), nullable=True, index=True)
    opponent_hurtbox_class = Column(String(64), nullable=True, index=True)  # UNIVERSAL, MALE_STANDARD, FEMALE_COMPACT, BIG, BEARS

    # Compatibility Status Ranking:
    # 1. VERIFIED_FOR_OPPONENT (tested in lab on this opponent)
    # 2. TESTED_UNDER_CONDITIONS (tested with specific distance/timing)
    # 3. REPORTED_UNTESTED (community reported, pending independent lab test)
    # 4. UNKNOWN_COMPATIBILITY (default when unrecorded; never assume incompatible)
    # 5. INCOMPATIBLE_DOCUMENTED (known/documented to drop on this opponent or hurtbox)
    compatibility_status = Column(String(32), nullable=False, default="UNKNOWN_COMPATIBILITY", index=True)

    is_compatible = Column(Boolean, nullable=False, default=True)
    timing_adjustment = Column(String(64), nullable=True)  # STANDARD, STRICT_MICRO_DASH, DELAYED_ENDER, DEEP_CROUCH_CANCEL, NONE
    incompatibility_reason = Column(Text, nullable=True)
    conditions_notes = Column(Text, nullable=True)
    verification_source = Column(String(128), nullable=False, default="Tekken 8 Lab / wavu.wiki")
    patch_version = Column(String(32), nullable=False, default="3.00.02")

    combo_route = relationship("ComboRoute", back_populates="compatibilities")
    opponent_character = relationship("Character")
