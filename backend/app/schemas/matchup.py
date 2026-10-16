from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.stage import StageRead


class MatchupConditions(BaseModel):
    wall_position: str = Field(default="OPEN", description="OPEN, NEAR_WALL, or CORNER")
    heat_state: str = Field(default="AVAILABLE", description="AVAILABLE, IN_HEAT, or SPENT")
    starting_distance: str = Field(default="MID", description="CLOSE, MID, or FAR")
    player_side: str = Field(default="P1", description="P1 or P2")


class MatchupRequest(BaseModel):
    player_character_id: int
    opponent_character_id: int
    stage_id: int
    conditions: Optional[MatchupConditions] = None
    session_token: Optional[str] = None


class PunishOption(BaseModel):
    opponent_move_name: str
    opponent_move_input: str
    opponent_block_advantage: int
    recommended_punish_name: str
    recommended_punish_input: str
    punish_startup: int
    damage: Optional[int] = None
    punish_tier: str
    punish_type: str
    stance_requirement: str = Field(default="STANDING", description="STANDING, WHILE_STANDING, or CROUCHING")
    verification_status: str = Field(default="GUARANTEED", description="GUARANTEED, CONDITIONAL, or UNVERIFIED")
    conditions_note: Optional[str] = Field(default=None, description="Tactical explanation or spacing limitation")
    hit_level: Optional[str] = Field(default=None, description="Opponent move hit level")
    pushback_risk: str = Field(default="NORMAL", description="MINIMAL, NORMAL, or HIGH")


class KeyMoveInfo(BaseModel):
    move_name: str
    input: str
    startup_frames: Optional[int] = None
    block_advantage: Optional[int] = None
    damage: Optional[int] = None
    hit_level: Optional[str] = None
    role: str
    properties: List[str] = []


class ComboRecommendation(BaseModel):
    title: str
    notation: str
    damage: int
    hits: int
    difficulty: str
    synergy_reason: str
    uses_heat: bool = False
    uses_tornado: bool = False
    uses_wall: bool = False


class StageSynergyInfo(BaseModel):
    has_walls: bool
    wall_danger_level: str
    wall_mechanics: List[str]
    floor_mechanics: List[str]
    transition_notes: Optional[str]
    tactical_advice: str


class OverallAssessment(BaseModel):
    rating: str = Field(description="FAVORABLE, EVEN, UNFAVORABLE, or INSUFFICIENT_DATA")
    rating_label: str = Field(description="Display label e.g. Favorable, Even, Unfavorable, Insufficient Data")
    rating_color: str = Field(description="Color class: success, info, warning, danger, neutral")
    reasoning: str = Field(description="Textual explanation supporting the assessment")
    confidence_level: str = Field(description="HIGH, MEDIUM, LOW, or NONE")
    confidence_score: int = Field(description="0 to 100 confidence score grounded in verified data")
    evidence_sources: List[str] = Field(default_factory=list, description="List of verified data sources")
    unknowns: List[str] = Field(default_factory=list, description="List of unverified or pending test elements")


class UsefulMoveRecommendation(BaseModel):
    move_name: str
    input: str
    startup_frames: Optional[int] = None
    block_advantage: Optional[int] = None
    hit_level: Optional[str] = None
    damage: Optional[int] = None
    role: str
    tactical_purpose: str


class DangerousOpponentMove(BaseModel):
    move_name: str
    input: str
    block_advantage: Optional[int] = None
    startup_frames: Optional[int] = None
    risk_level: str = Field(description="EXTREME, HIGH, or MEDIUM")
    threat_description: str
    recommended_counter: str


class SpacingMovementInfo(BaseModel):
    optimal_range: str
    neutral_strategy: str
    approach_advice: str
    retreat_spacing: str


class DefensiveTacticsInfo(BaseModel):
    punish_matrix: List[PunishOption]
    fuzzy_guard_notes: Optional[str] = None
    interrupt_opportunities: Optional[str] = None
    low_defense_priority: str


class SidestepTrackingInfo(BaseModel):
    recommended_side: str  # SSL, SSR, SWR, SWL, NEUTRAL
    side_label: str
    reasoning: str
    linear_moves_to_step: List[str] = Field(default_factory=list)
    opponent_homing_moves: List[str] = Field(default_factory=list)


class HeatMechanicsInfo(BaseModel):
    player_heat_focus: str
    opponent_heat_threats: str
    heat_smash_interaction: str
    stance_and_install_dynamics: str


class StageMatchupInfo(BaseModel):
    has_walls: bool
    wall_danger_level: str
    wall_mechanics: List[str]
    floor_mechanics: List[str]
    transition_notes: Optional[str] = None
    tactical_advice: str
    character_stage_advantage: str


class DirectionalProvenance(BaseModel):
    direction: str
    player_character_name: str
    opponent_character_name: str
    patch_version: str
    contributor: str
    verification_status: str
    last_reviewed: Optional[str] = None


class MatchupOverviewResponse(BaseModel):
    # Phase 1 fields (preserved)
    player_character: CharacterRead
    opponent_character: CharacterRead
    stage: StageRead
    conditions: MatchupConditions
    punish_matrix: List[PunishOption]
    player_key_moves: List[KeyMoveInfo]
    stage_synergy: StageSynergyInfo
    suitable_combos: List[ComboRecommendation]
    strengths: List[str]
    weaknesses: List[str]
    matchup_notes: str
    has_specific_lab_notes: bool
    data_completeness: Dict[str, Any]

    # Phase 2 10-Section Intelligence
    overall_assessment: OverallAssessment
    player_strengths: List[str]
    opponent_strengths: List[str]
    useful_moves: List[UsefulMoveRecommendation]
    dangerous_moves: List[DangerousOpponentMove]
    spacing_and_movement: SpacingMovementInfo
    defensive_tactics: DefensiveTacticsInfo
    sidestep_and_tracking: SidestepTrackingInfo
    heat_and_mechanics: HeatMechanicsInfo
    stage_matchup_synergy: StageMatchupInfo
    directional_provenance: DirectionalProvenance

    # Phase 2 Complete Two-Player Matchup Additions
    p1_punish_matrix: List[PunishOption] = Field(default_factory=list, description="P1 punish options against P2 moves")
    p2_punish_matrix: List[PunishOption] = Field(default_factory=list, description="P2 punish options against P1 moves")
    opponent_key_moves: List[KeyMoveInfo] = Field(default_factory=list, description="P2 Key signature moves")
    opponent_suitable_combos: List[ComboRecommendation] = Field(default_factory=list, description="P2 Recommended combos")

    # Master Compendium Pro Tactics & Relativity (Parts 5, 8, 14, 19, 22, 23)
    opponent_sidestep_guide: Optional[Dict[str, Any]] = Field(default=None, description="Opponent weak sidestep and linear moves to step (Part 5)")
    opponent_throw_break_guide: Optional[Dict[str, Any]] = Field(default=None, description="Opponent command throw break cues and break buttons (Part 8)")
    opponent_anti_cheese_guide: Optional[Dict[str, Any]] = Field(default=None, description="Opponent spammed cheese strings and guaranteed counter (Part 14)")
    opponent_install_guide: Optional[Dict[str, Any]] = Field(default=None, description="Opponent unique install/buff meters & critical threat windows (Part 23)")
    opponent_ten_hit_guide: Optional[Dict[str, Any]] = Field(default=None, description="Opponent 10-hit combo string interrupt/parry timing (Part 19)")
    player_wall_combo_guide: Optional[Dict[str, Any]] = Field(default=None, description="Player optimal wall combo ender and tornado utilization (Part 22)")



class PreferencePayload(BaseModel):
    session_token: str
    player_character_id: Optional[int] = None
    opponent_character_id: Optional[int] = None
    stage_id: Optional[int] = None
    conditions: Optional[MatchupConditions] = None

