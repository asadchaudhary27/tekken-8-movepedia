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


class MatchupOverviewResponse(BaseModel):
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


class PreferencePayload(BaseModel):
    session_token: str
    player_character_id: Optional[int] = None
    opponent_character_id: Optional[int] = None
    stage_id: Optional[int] = None
    conditions: Optional[MatchupConditions] = None
