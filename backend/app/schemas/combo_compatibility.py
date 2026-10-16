from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.stage import StageRead


class ComboScalingHit(BaseModel):
    hit_number: int
    move_notation: str
    move_name: Optional[str] = None
    raw_damage: int
    scaling_percent: int  # e.g. 100, 70, 50, 40, 30
    scaled_damage: int
    notes: Optional[str] = None


class DamageCalculationRequest(BaseModel):
    hits: List[Dict[str, Any]]
    is_counter_hit: bool = False
    tested_damage: Optional[int] = None
    damage_type: str = "TESTED"
    calculation_method: str = "LAB_TESTED_IN_GAME"


class DamageCalculationResult(BaseModel):
    tested_damage: Optional[int] = None
    raw_damage_sum: int
    scaled_damage_total: int
    is_estimate: bool = False
    damage_type: str = "TESTED"  # TESTED, REPORTED, ESTIMATED, UNVERIFIED
    calculation_method: str = "LAB_TESTED_IN_GAME"
    scaling_formula_explanation: str
    hits: List[ComboScalingHit] = Field(default_factory=list)


class ComboCompatibilityRecordRead(BaseModel):
    id: Optional[int] = None
    combo_route_id: int
    opponent_character_id: Optional[int] = None
    opponent_character_name: Optional[str] = None
    opponent_hurtbox_class: Optional[str] = None
    compatibility_status: str = "UNKNOWN_COMPATIBILITY"
    is_compatible: bool = True
    timing_adjustment: Optional[str] = None
    incompatibility_reason: Optional[str] = None
    conditions_notes: Optional[str] = None
    verification_source: str = "Tekken 8 Lab / wavu.wiki"
    patch_version: str = "3.00.02"

    model_config = ConfigDict(from_attributes=True)


class ComboDetailedRead(BaseModel):
    id: int
    character_id: int
    title: str
    notation_sequence: str
    total_damage: int = 0
    hit_count: int = 0
    difficulty: str = "MEDIUM"
    combo_type: str = "MIDSCREEN"
    launcher_type: str = "NORMAL_HIT"

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

    damage_type: str = "TESTED"  # TESTED, REPORTED, ESTIMATED, UNVERIFIED
    damage_calculation_method: str = "LAB_TESTED_IN_GAME"
    is_damage_estimate: bool = False
    raw_damage_sum: Optional[int] = None
    scaling_breakdown: List[ComboScalingHit] = Field(default_factory=list)

    required_stance: Optional[str] = None
    execution_notes: Optional[str] = None
    target_hurtbox_class: str = "UNIVERSAL"

    easier_alternative_id: Optional[int] = None
    easier_alternative_title: Optional[str] = None
    easier_alternative_notes: Optional[str] = None

    # Computed dynamic compatibility for currently selected rival
    compatibility_status: str = "UNKNOWN_COMPATIBILITY"
    compatibility_badge_class: str = "unknown"
    timing_adjustment: Optional[str] = None
    incompatibility_reason: Optional[str] = None

    # Computed dynamic stage compatibility for currently selected battleground
    is_stage_compatible: bool = True
    stage_compatibility_status: str = "SUPPORTED"  # SUPPORTED, UNAVAILABLE_ON_STAGE, ALTERNATIVE_AVAILABLE, UNKNOWN
    stage_incompatibility_reason: Optional[str] = None
    alternative_route_id: Optional[int] = None
    alternative_route_title: Optional[str] = None
    alternative_route_notation: Optional[str] = None
    alternative_route_damage: Optional[int] = None

    conditions_notes: Optional[str] = None
    source: str = "TekkenDocs / Community Verified Lab"
    verification_status: str = "VERIFIED"
    patch_version: str = "3.00.02"

    model_config = ConfigDict(from_attributes=True)


class OpponentHurtboxInfo(BaseModel):
    character_id: int
    character_name: str
    hurtbox_class: str  # MALE_STANDARD, FEMALE_COMPACT, BIG, BEARS
    description: str
    known_quirks: List[str] = Field(default_factory=list)


class ComboRecommendationReport(BaseModel):
    player_character: CharacterRead
    opponent_character: CharacterRead
    opponent_hurtbox: OpponentHurtboxInfo
    stage: Optional[StageRead] = None
    stage_name: Optional[str] = None
    stage_has_walls: Optional[bool] = None
    stage_wall_break_supported: Optional[bool] = None
    stage_floor_break_supported: Optional[bool] = None
    stage_balcony_break_supported: Optional[bool] = None
    stage_warnings: List[str] = Field(default_factory=list)
    stage_supported_combos_count: int = 0
    stage_unmet_combos_count: int = 0
    wall_position: str = "OPEN"
    heat_state: str = "AVAILABLE"

    total_combos_analyzed: int = 0
    compatibility_breakdown: Dict[str, int] = Field(default_factory=dict)

    # 10 Recommendation categories requested in Phase 5 prompt:
    beginner_friendly: List[ComboDetailedRead] = Field(default_factory=list)
    standard_launch: List[ComboDetailedRead] = Field(default_factory=list)
    high_damage_optimal: List[ComboDetailedRead] = Field(default_factory=list)
    wall_carry: List[ComboDetailedRead] = Field(default_factory=list)
    wall_combo: List[ComboDetailedRead] = Field(default_factory=list)
    heat_dependent: List[ComboDetailedRead] = Field(default_factory=list)
    counter_hit: List[ComboDetailedRead] = Field(default_factory=list)
    character_specific: List[ComboDetailedRead] = Field(default_factory=list)
    stage_break: List[ComboDetailedRead] = Field(default_factory=list)
    alternative_routes: List[ComboDetailedRead] = Field(default_factory=list)

    damage_scaling_rules_explanation: str
    provenance_notes: str
    patch_version: str = "3.00.02"
