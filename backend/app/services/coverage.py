"""
Data Completeness & Quality Coverage Reporting Service.
Audits database records and import payloads against academic quality standards.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
import json
import csv
import os
from sqlalchemy.orm import Session
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.conflict import DataConflict
from backend.app.schemas.coverage import (
    CoverageReportResponse,
    RosterSummary,
    MoveSummary,
    FieldCoverageMetrics,
    DeficiencyBreakdown,
    UnsupportedTokenEntry,
    SourceAuditEntry,
    CharacterCoverageDetail
)
from backend.app.services.notation import NotationEngine

# Canonical T8 Roster Reference (Base + Season DLCs as verified in tekkendocs & tekken8combo)
EXPECTED_ROSTER = [
    "alisa", "anna", "armor-king", "asuka", "azucena", "bob", "bryan", "claudio",
    "clive", "devil-jin", "dragunov", "eddy", "fahkumram", "feng", "heihachi",
    "hwoarang", "jack-8", "jin", "jun", "kazuya", "king", "kuma", "kunimitsu",
    "lars", "law", "lee", "leo", "leroy", "lidia", "lili", "miary-zo", "nina",
    "panda", "paul", "raven", "reina", "roger-jr", "shaheen", "steve", "victor",
    "xiaoyu", "yoshimitsu", "zafina"
]


class CoverageReportingService:
    """Computes field-level coverage metrics and deficiency audits."""

    @classmethod
    def generate_report(cls, db: Session, patch_version: str = "3.00.02") -> CoverageReportResponse:
        characters = db.query(Character).all()
        char_slugs = {c.slug for c in characters}
        missing_chars = [slug for slug in EXPECTED_ROSTER if slug not in char_slugs]

        expected_count = len(EXPECTED_ROSTER)
        ingested_char_count = len(characters)
        roster_coverage_pct = round((ingested_char_count / expected_count) * 100, 2) if expected_count else 0.0

        all_moves = db.query(Move).all()
        total_moves = len(all_moves)
        avg_moves = round(total_moves / ingested_char_count, 2) if ingested_char_count else 0.0

        unverified_count = sum(1 for m in all_moves if m.verification_status != "VERIFIED")
        conflicts_count = db.query(DataConflict).filter(DataConflict.resolution_status == "UNRESOLVED").count()

        # Duplicate check (char_id, normalized_notation)
        seen_keys = set()
        duplicate_count = 0
        for m in all_moves:
            key = (m.character_id, m.normalized_notation)
            if key in seen_keys:
                duplicate_count += 1
            else:
                seen_keys.add(key)

        # Field coverage calculations
        # Required fields: input_notation, startup_frames, block_advantage, damage, hit_level
        # Optional fields: hit_advantage, ch_advantage, name, stance_context
        pop_input = sum(1 for m in all_moves if m.normalized_notation)
        pop_startup = sum(1 for m in all_moves if m.startup_frames is not None)
        pop_block = sum(1 for m in all_moves if m.block_advantage is not None)
        pop_damage = sum(1 for m in all_moves if m.damage is not None)
        pop_hit_level = sum(1 for m in all_moves if m.hit_level)

        pop_hit_adv = sum(1 for m in all_moves if m.hit_advantage is not None or m.hit_advantage_raw)
        pop_ch_adv = sum(1 for m in all_moves if m.ch_advantage is not None or m.ch_advantage_raw)
        pop_name = sum(1 for m in all_moves if m.name)
        pop_stance = sum(1 for m in all_moves if m.stance_context)

        denom = total_moves if total_moves > 0 else 1

        req_metrics = {
            "input_notation": round((pop_input / denom) * 100, 2),
            "startup_frames": round((pop_startup / denom) * 100, 2),
            "block_advantage": round((pop_block / denom) * 100, 2),
            "damage": round((pop_damage / denom) * 100, 2),
            "hit_level": round((pop_hit_level / denom) * 100, 2),
        }

        opt_metrics = {
            "hit_advantage": round((pop_hit_adv / denom) * 100, 2),
            "counter_hit_advantage": round((pop_ch_adv / denom) * 100, 2),
            "move_name": round((pop_name / denom) * 100, 2),
            "stance_context": round((pop_stance / denom) * 100, 2),
        }

        overall_pct = round(sum(req_metrics.values()) / len(req_metrics), 2) if req_metrics else 0.0

        # Audit unsupported notation tokens
        unsupported_tokens_map: Dict[str, Dict[str, Any]] = {}
        for m in all_moves:
            conv = NotationEngine.convert(m.original_notation)
            for uns in conv.unsupported_tokens:
                if uns not in unsupported_tokens_map:
                    unsupported_tokens_map[uns] = {"count": 0, "example": m.original_notation}
                unsupported_tokens_map[uns]["count"] += 1

        unsupported_entries = [
            UnsupportedTokenEntry(token=k, count=v["count"], example_move=v["example"])
            for k, v in unsupported_tokens_map.items()
        ]

        # Per-character details
        char_details: List[CharacterCoverageDetail] = []
        for c in characters:
            c_moves = [m for m in all_moves if m.character_id == c.id]
            c_total = len(c_moves)
            c_denom = c_total if c_total > 0 else 1
            char_details.append(
                CharacterCoverageDetail(
                    character_slug=c.slug,
                    character_name=c.name,
                    total_moves=c_total,
                    startup_coverage_pct=round((sum(1 for m in c_moves if m.startup_frames is not None) / c_denom) * 100, 2),
                    block_coverage_pct=round((sum(1 for m in c_moves if m.block_advantage is not None) / c_denom) * 100, 2),
                    hit_coverage_pct=round((sum(1 for m in c_moves if m.hit_advantage is not None or m.hit_advantage_raw) / c_denom) * 100, 2),
                    ch_coverage_pct=round((sum(1 for m in c_moves if m.ch_advantage is not None or m.ch_advantage_raw) / c_denom) * 100, 2),
                    damage_coverage_pct=round((sum(1 for m in c_moves if m.damage is not None) / c_denom) * 100, 2),
                    unverified_count=sum(1 for m in c_moves if m.verification_status != "VERIFIED"),
                    conflict_count=sum(len(m.conflicts) for m in c_moves)
                )
            )

        report_id = f"cov-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

        return CoverageReportResponse(
            report_id=report_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            game_patch=patch_version,
            roster_summary=RosterSummary(
                expected_roster_count=expected_count,
                ingested_character_count=ingested_char_count,
                roster_coverage_percentage=roster_coverage_pct,
                missing_characters=missing_chars
            ),
            move_summary=MoveSummary(
                total_moves_ingested=total_moves,
                average_moves_per_character=avg_moves,
                duplicate_records_detected=duplicate_count,
                unverified_records=unverified_count,
                conflicting_records=conflicts_count
            ),
            field_coverage=FieldCoverageMetrics(
                required_fields=req_metrics,
                optional_fields=opt_metrics,
                overall_field_coverage_percentage=overall_pct
            ),
            deficiency_breakdown=DeficiencyBreakdown(
                missing_required_count=(denom * 5) - (pop_input + pop_startup + pop_block + pop_damage + pop_hit_level) if total_moves else 0,
                not_provided_count=sum(1 for m in all_moves if m.damage is None),
                inapplicable_count=sum(1 for m in all_moves if m.hit_level in ["t", "ub"] and m.block_advantage is None),
                unknown_value_count=sum(1 for m in all_moves if m.block_advantage is None),
                unsupported_notation_tokens=unsupported_entries
            ),
            data_sources_audited=[
                SourceAuditEntry(source_name="wavu_wiki", status="APPROVED", records_provided=total_moves, conflicts_count=conflicts_count),
                SourceAuditEntry(source_name="tekkendocs", status="APPROVED_WITH_RESTRICTIONS", records_provided=0, conflicts_count=0)
            ],
            character_breakdowns=char_details
        )

    @classmethod
    def export_report_files(cls, report: CoverageReportResponse, reports_dir: str = "data/reports") -> Tuple[str, str]:
        os.makedirs(reports_dir, exist_ok=True)
        json_path = os.path.join(reports_dir, f"{report.report_id}.json")
        csv_path = os.path.join(reports_dir, f"{report.report_id}.csv")

        # Export JSON
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        # Export CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "character_slug", "character_name", "total_moves",
                "startup_coverage_pct", "block_coverage_pct", "hit_coverage_pct",
                "ch_coverage_pct", "damage_coverage_pct", "unverified_count", "conflict_count"
            ])
            for d in report.character_breakdowns:
                writer.writerow([
                    d.character_slug, d.character_name, d.total_moves,
                    d.startup_coverage_pct, d.block_coverage_pct, d.hit_coverage_pct,
                    d.ch_coverage_pct, d.damage_coverage_pct, d.unverified_count, d.conflict_count
                ])

        return json_path, csv_path
