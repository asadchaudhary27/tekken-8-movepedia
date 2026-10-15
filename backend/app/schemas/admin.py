from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class QualityDashboardStats(BaseModel):
    total_characters: int
    total_stages: int
    total_moves: int
    total_combos: int
    total_verification_records: int

    missing_frame_data_count: int
    missing_stage_mechanics_count: int
    combos_without_opponent_compatibility_count: int
    unverified_punish_options_count: int
    conflicting_records_count: int
    outdated_patch_records_count: int
    incomplete_source_metadata_count: int
    records_awaiting_review_count: int

    status_distribution: Dict[str, int] = Field(default_factory=dict)
    audit_issues: List[Dict[str, Any]] = Field(default_factory=list)


class VerificationRecordRead(BaseModel):
    id: int
    entity_type: str
    entity_id: Optional[int] = None
    field_name: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    verified_by: str
    method: str
    result: str
    evidence_notes: Optional[str] = None
    change_summary: Optional[str] = None
    patch_version: str
    source_url: Optional[str] = None
    verified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatusUpdateRequest(BaseModel):
    entity_type: str  # MOVE, COMBO, MATCHUP_NOTE, COMPATIBILITY, STAGE, PUNISH
    entity_id: int
    new_status: str   # VERIFIED, UNVERIFIED, CONFLICTING, UNAVAILABLE, CONFIRMED_ABSENT
    evidence_notes: str
    source_url: Optional[str] = None
    patch_version: str = "3.00.02"


class MoveAdminCreateUpdate(BaseModel):
    character_id: int
    name: str
    normalized_notation: str
    original_notation: Optional[str] = None
    startup_frames: Optional[int] = None
    block_advantage: Optional[int] = None
    hit_advantage: Optional[int] = None
    ch_advantage: Optional[int] = None
    damage: Optional[int] = None
    hit_level: Optional[str] = None
    stance_context: Optional[str] = None
    verification_status: str = "VERIFIED"
    verification_notes: Optional[str] = None
    patch_version: str = "3.00.02"
    source_name: str = "Admin Manual Input"
    source_url: Optional[str] = None
    reason_for_change: str = "Manual Admin Edit"


class ComboAdminCreateUpdate(BaseModel):
    id: Optional[int] = None
    character_id: int
    title: str
    notation_sequence: str
    total_damage: int
    hit_count: int
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
    damage_type: str = "TESTED"
    damage_calculation_method: str = "LAB_TESTED_IN_GAME"
    raw_damage_sum: Optional[int] = None
    required_stance: Optional[str] = None
    execution_notes: Optional[str] = None
    target_hurtbox_class: str = "UNIVERSAL"
    easier_alternative_id: Optional[int] = None
    easier_alternative_notes: Optional[str] = None
    verification_status: str = "VERIFIED"
    patch_version: str = "3.00.02"
    source: str = "Community Verified Lab"
    reason_for_change: str = "Manual Admin Edit"


class StageMechanicsAdminUpdate(BaseModel):
    stage_id: int
    has_walls: bool = True
    boundary_shape: Optional[str] = None
    wall_distance: Optional[str] = None
    wall_break: bool = False
    hard_wall_break: bool = False
    wall_blast: bool = False
    floor_break: bool = False
    floor_blast: bool = False
    balcony_break: bool = False
    special_mechanics: Optional[str] = None
    notes: Optional[str] = None
    reason_for_change: str = "Stage mechanics update"


class MatchupNoteAdminUpdate(BaseModel):
    player_character_id: int
    opponent_character_id: int
    stage_id: Optional[int] = None
    overview: Optional[str] = None
    key_advice: Optional[str] = None
    rating: str = "EVEN"
    confidence_level: str = "MEDIUM"
    confidence_score: int = 50
    spacing_and_movement: Optional[str] = None
    defensive_options: Optional[str] = None
    sidestep_and_tracking: Optional[str] = None
    heat_and_mechanics: Optional[str] = None
    stage_considerations: Optional[str] = None
    verification_status: str = "VERIFIED"
    patch_version: str = "3.00.02"
    reason_for_change: str = "Matchup intelligence update"


class CompatibilityAdminUpdate(BaseModel):
    combo_route_id: int
    opponent_character_id: Optional[int] = None
    opponent_hurtbox_class: Optional[str] = None
    compatibility_status: str = "TESTED_UNDER_CONDITIONS"
    is_compatible: bool = True
    timing_adjustment: Optional[str] = None
    incompatibility_reason: Optional[str] = None
    conditions_notes: Optional[str] = None
    verification_source: str = "Tekken 8 Lab / wavu.wiki"
    patch_version: str = "3.00.02"
    reason_for_change: str = "Compatibility update"


class DataSourceCreateUpdate(BaseModel):
    name: str
    base_url: str
    license_type: str
    attribution_text: Optional[str] = None
    license_url: Optional[str] = None
    approval_status: str = "APPROVED_FOR_USE"
    rate_limit_policy: str = "1 request / sec"
    is_active: bool = True


class GamePatchCreateUpdate(BaseModel):
    version_number: str
    release_date: Optional[str] = None
    notes: Optional[str] = None
    is_current: bool = False


class ImportRowIssue(BaseModel):
    row_index: int
    issue_type: str  # ERROR, WARNING, DUPLICATE, CONFLICT, UNVERIFIED_OVERWRITE_PROTECTED
    field: Optional[str] = None
    message: str
    incoming_data: Dict[str, Any] = Field(default_factory=dict)


class ImportPreviewRequest(BaseModel):
    entity_type: str  # MOVES, COMBOS, STAGES, COMPATIBILITY, MATCHUP_NOTES
    format: str = "JSON"  # JSON, CSV
    raw_content: str
    source_name: str = "Manual Import"
    source_url: Optional[str] = None
    patch_version: str = "3.00.02"
    field_mapping: Optional[Dict[str, str]] = None


class ImportPreviewResponse(BaseModel):
    entity_type: str
    total_rows: int
    valid_rows_count: int
    error_rows_count: int
    duplicate_count: int
    conflict_count: int
    verified_protection_count: int
    is_importable: bool
    preview_rows: List[Dict[str, Any]] = Field(default_factory=list)
    issues: List[ImportRowIssue] = Field(default_factory=list)


class ImportExecuteRequest(BaseModel):
    entity_type: str  # MOVES, COMBOS, STAGES, COMPATIBILITY, MATCHUP_NOTES
    rows: List[Dict[str, Any]]
    source_name: str = "Manual Import"
    source_url: Optional[str] = None
    patch_version: str = "3.00.02"
    allow_override_verified: bool = False


class ImportSummaryResponse(BaseModel):
    success: bool
    entity_type: str
    total_submitted: int
    records_created: int
    records_updated: int
    records_skipped: int
    conflicts_logged: int
    audit_records_created: int
    rollback_occurred: bool
    message: str
    error_details: Optional[str] = None
