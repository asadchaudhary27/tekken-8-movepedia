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
    launcher_type: str = "NORMAL_HIT"  # NORMAL_HIT, COUNTER_HIT, WHILE_RISING, CROUCH, TORNADO_STARTER, STUN, PUNISH
    damage_type: str = "TESTED"  # TESTED, REPORTED, ESTIMATED, UNVERIFIED
    damage_calculation_method: str = "LAB_TESTED_IN_GAME"  # LAB_TESTED_IN_GAME, REPORTED_SOURCE, SCALED_ESTIMATE, UNVERIFIED
    raw_damage_sum: Optional[int] = None
    scaling_breakdown_json: Optional[str] = None
    execution_notes: Optional[str] = None
    required_stance: Optional[str] = None
    target_hurtbox_class: str = "UNIVERSAL"
    easier_alternative_id: Optional[int] = None
    easier_alternative_notes: Optional[str] = None
    verification_status: str = "VERIFIED"
    patch_version: str = "3.00.02"


class ComboRouteCreate(ComboRouteBase):
    character_id: int
    starter_move_id: Optional[int] = None


class ComboRouteRead(ComboRouteBase):
    id: int
    character_id: int
    starter_move_id: Optional[int] = None
    character: Optional[CharacterRead] = None
    stage: Optional[StageRead] = None
    character_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ComboBenchmarkComparison(BaseModel):
    combo_a: ComboRouteRead
    combo_b: ComboRouteRead
    damage_difference: int  # a - b
    hit_difference: int  # a - b
    damage_per_hit_a: float
    damage_per_hit_b: float
    is_directly_comparable: bool
    comparability_notes: str
    practicality_comparison: str


class ComboFilterParams(BaseModel):
    character_id: Optional[int] = None
    character_slug: Optional[str] = None
    stage_id: Optional[int] = None
    stage_slug: Optional[str] = None
    combo_type: Optional[str] = None  # ALL, MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK
    requires_heat: Optional[bool] = None
    requires_ch: Optional[bool] = None
    difficulty: Optional[str] = None
    launcher_type: Optional[str] = None
    min_damage: Optional[int] = None
    max_damage: Optional[int] = None
    uses_wall: Optional[bool] = None
    uses_tornado: Optional[bool] = None
    is_stage_dependent: Optional[bool] = None
    required_stance: Optional[str] = None
    verification_status: Optional[str] = None
    target_hurtbox_class: Optional[str] = None
    stage_section: Optional[str] = None
    query: Optional[str] = None
