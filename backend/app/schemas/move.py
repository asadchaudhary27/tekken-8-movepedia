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
    stable_source_id: Optional[str] = None
    properties: List[MovePropertySchema] = []
    inputs: List[MoveInputSchema] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
