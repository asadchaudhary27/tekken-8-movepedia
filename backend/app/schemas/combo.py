from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.stage import StageRead


class ComboRouteBase(BaseModel):
    title: str
    notation_sequence: str
    total_damage: int = 0
    hit_count: int = 0
    difficulty: str = "MEDIUM"  # EASY, MEDIUM, HARD, OPTIMAL
    combo_type: str = "MIDSCREEN"  # MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK
    uses_heat: bool = False
    uses_tornado: bool = False
    uses_wall: bool = False
    requires_counter_hit: bool = False
    is_stage_dependent: bool = False
    stage_id: Optional[int] = None
    stage_section: Optional[str] = None
    starter_move_name: Optional[str] = None
    starter_move_input: Optional[str] = None
    ender_move_name: Optional[str] = None
    ender_move_input: Optional[str] = None
    conditions_notes: Optional[str] = None
    source: str = "TekkenDocs / Community Verified Lab"


class ComboRouteCreate(ComboRouteBase):
    character_id: int
    starter_move_id: Optional[int] = None


class ComboRouteRead(ComboRouteBase):
    id: int
    character_id: int
    starter_move_id: Optional[int] = None
    character: Optional[CharacterRead] = None
    stage: Optional[StageRead] = None

    model_config = ConfigDict(from_attributes=True)


class ComboFilterParams(BaseModel):
    character_id: Optional[int] = None
    character_slug: Optional[str] = None
    stage_id: Optional[int] = None
    stage_slug: Optional[str] = None
    combo_type: Optional[str] = None  # ALL, MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK
    requires_heat: Optional[bool] = None
    requires_ch: Optional[bool] = None
    difficulty: Optional[str] = None
    stage_section: Optional[str] = None
