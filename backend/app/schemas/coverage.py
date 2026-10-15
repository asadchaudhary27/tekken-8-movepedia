from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class RosterSummary(BaseModel):
    expected_roster_count: int
    ingested_character_count: int
    roster_coverage_percentage: float
    missing_characters: List[str] = []


class MoveSummary(BaseModel):
    total_moves_ingested: int
    average_moves_per_character: float
    duplicate_records_detected: int
    unverified_records: int
    conflicting_records: int


class FieldCoverageMetrics(BaseModel):
    required_fields: Dict[str, float]
    optional_fields: Dict[str, float]
    overall_field_coverage_percentage: float


class UnsupportedTokenEntry(BaseModel):
    token: str
    count: int
    example_move: Optional[str] = None


class DeficiencyBreakdown(BaseModel):
    missing_required_count: int
    not_provided_count: int
    inapplicable_count: int
    unknown_value_count: int
    unsupported_notation_tokens: List[UnsupportedTokenEntry] = []


class SourceAuditEntry(BaseModel):
    source_name: str
    status: str
    records_provided: int
    conflicts_count: int = 0


class CharacterCoverageDetail(BaseModel):
    character_slug: str
    character_name: str
    total_moves: int
    startup_coverage_pct: float
    block_coverage_pct: float
    hit_coverage_pct: float
    ch_coverage_pct: float
    damage_coverage_pct: float
    unverified_count: int
    conflict_count: int


class CoverageReportResponse(BaseModel):
    report_id: str
    generated_at: str
    game_patch: str
    roster_summary: RosterSummary
    move_summary: MoveSummary
    field_coverage: FieldCoverageMetrics
    deficiency_breakdown: DeficiencyBreakdown
    data_sources_audited: List[SourceAuditEntry]
    character_breakdowns: List[CharacterCoverageDetail] = []
