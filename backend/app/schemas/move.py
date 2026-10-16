from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MovePropertySchema(BaseModel):
    property_type: str
    value: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MoveInputSchema(BaseModel):
    sequence_index: int
    direction_code: str
    buttons_raw: str
    is_simultaneous: bool = False
    is_hold: bool = False
    is_just_frame: bool = False
    stance_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MoveBase(BaseModel):
    name: Optional[str] = None
    original_notation: str
    normalized_notation: str
    startup_frames: Optional[int] = None
    startup_raw: Optional[str] = None
    block_advantage: Optional[int] = None
    block_advantage_raw: Optional[str] = None
    hit_advantage: Optional[int] = None
    hit_advantage_raw: Optional[str] = None
    ch_advantage: Optional[int] = None
    ch_advantage_raw: Optional[str] = None
    damage: Optional[int] = None
    damage_raw: Optional[str] = None
    hit_level: Optional[str] = None
    stance_context: Optional[str] = None
    verification_status: str = "UNVERIFIED"
    verification_notes: Optional[str] = None


class MoveCreate(MoveBase):
    character_id: int
    stable_source_id: Optional[str] = None
    patch_id: Optional[int] = None
    import_batch_id: Optional[int] = None
    properties: Optional[List[str]] = []


class MoveResponse(MoveBase):
    id: int
    character_id: int
    character_name: Optional[str] = None
    character_slug: Optional[str] = None
    stable_source_id: Optional[str] = None

    # Analytical Frame & Safety Attributes
    hit_level_type: Optional[str] = None
    block_safety: Optional[str] = None  # SAFE, UNSAFE, LAUNCH_PUNISH, PLUS, NOT_APPLICABLE, UNKNOWN
    punish_recommendation: Optional[str] = None
    punish_startup_min: Optional[int] = None
    punish_window_frames: Optional[int] = None
    punish_window_type: Optional[str] = None
    has_pushback: bool = False
    pushback_warning: Optional[str] = None
    is_launch_punishable: bool = False
    is_plus_on_block: bool = False
    is_homing: bool = False
    is_tornado: bool = False
    is_heat_engager: bool = False
    is_power_crush: bool = False
    is_counter_hit_launcher: bool = False
    is_stance_move: bool = False
    is_stance_transition: bool = False
    is_from_stance: bool = False
    stance_name: Optional[str] = None
    transition_stance: Optional[str] = None
    recovery_frames: Optional[int] = None
    recovery_raw: Optional[str] = None
    tracking_property: Optional[str] = None
    defensive_response: Optional[str] = None
    conditional_notes: Optional[str] = None
    frame_state_type: str = "VERIFIED"  # VERIFIED, CONDITIONAL, NOT_APPLICABLE, REPORTED, UNVERIFIED, UNKNOWN

    # Provenance and Version Tracking
    patch_version: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    last_verified_date: Optional[datetime] = None

    properties: List[MovePropertySchema] = []
    inputs: List[MoveInputSchema] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MoveSummaryStats(BaseModel):
    total_moves: int
    verified_count: int
    verified_percentage: float
    safe_moves_count: int
    unsafe_moves_count: int
    launch_punishable_count: int
    plus_on_block_count: int
    heat_engagers_count: int
    homing_count: int
    power_crush_count: int
