from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.schemas.character import CharacterRead


class PunishOptionDetail(BaseModel):
    opponent_move_id: int
    opponent_move_name: str
    opponent_move_input: str
    opponent_startup: Optional[int] = None
    opponent_block_advantage: Optional[int] = None
    opponent_hit_level: Optional[str] = None
    opponent_stance: Optional[str] = None
    opponent_recovery_state: str = Field(description="STANDING or CROUCHING")
    opponent_pushback: str = Field(default="NONE", description="NONE, LOW, MEDIUM, HIGH")
    is_punishable: bool = False
    is_launch_punishable: bool = False
    is_safe: bool = False
    punish_status: str = Field(description="GUARANTEED, CONDITIONAL, UNVERIFIED, or SAFE")
    recommended_punish_id: Optional[int] = None
    recommended_punish_name: Optional[str] = None
    recommended_punish_input: Optional[str] = None
    punish_startup: Optional[int] = None
    punish_damage: Optional[int] = None
    punish_hit_level: Optional[str] = None
    punish_state_required: str = Field(default="STANDING", description="STANDING, WHILE_STANDING, FULL_CROUCH, or NONE")
    punish_tier: str = Field(default="Safe Guard", description="i10 Jab, i12 Frame, i13 WS, Launch Punish, etc.")
    range_condition: str = Field(default="Standard Range")
    stance_requirement: Optional[str] = None
    why_it_works: str = Field(description="Beginner-friendly explanation of why and how this response works")
    confidence_score: int = Field(default=85)
    source: str = Field(default="TekkenDocs Patch 3.00.02")
    patch_version: str = Field(default="3.00.02")
    verification_status: str = Field(default="VERIFIED")


class PunishmentAssistantResponse(BaseModel):
    player_character: CharacterRead
    opponent_character: CharacterRead
    total_opponent_moves: int
    punishable_moves_count: int
    launch_punishable_count: int
    safe_moves_count: int
    options: List[PunishOptionDetail]
    patch_version: str = "3.00.02"


class PracticeAttemptPayload(BaseModel):
    session_token: str
    player_character_id: int
    opponent_character_id: int
    opponent_move_id: Optional[int] = None
    opponent_move_name: str
    opponent_move_input: str
    punish_move_input: str
    result: str = Field(description="SUCCESS or FAIL")


class PracticeRecordItem(BaseModel):
    id: int
    opponent_move_name: str
    opponent_move_input: str
    punish_move_input: str
    success_count: int
    fail_count: int
    attempts: int
    mastery_score: int
    last_practiced_at: Optional[str] = None


class PracticeProgressResponse(BaseModel):
    session_token: str
    total_attempts: int
    total_successes: int
    total_failures: int
    overall_accuracy_pct: float
    mastered_moves_count: int
    records: List[PracticeRecordItem]
