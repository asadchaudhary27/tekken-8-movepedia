"""
Local Test Fixture Adapter for Repeatable Ingestion & Offline Testing.
Loads verified Tekken 8 character move datasets from data/fixtures/ without live network calls.
"""

import json
import os
from typing import List, Any
from backend.app.services.adapters.base import (
    BaseSourceAdapter,
    NormalizedImportRecord,
    BatchImportReport
)
from backend.app.services.notation import NotationEngine


class LocalFixtureAdapter(BaseSourceAdapter):
    """Adapter reading from local validated JSON fixtures."""

    @property
    def source_name(self) -> str:
        return "local_test_fixture"

    @property
    def approval_status(self) -> str:
        return "APPROVED"

    @property
    def rate_limit_delay_seconds(self) -> float:
        return 0.0

    def fetch_raw_data(self, character_slug: str, fixture_path: str = "data/fixtures/sample_moves.json") -> Any:
        if not os.path.exists(fixture_path):
            return []
        with open(fixture_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [m for m in data if m.get("character_slug") == character_slug or character_slug == "all"]

    def parse_payload(self, raw_payload: Any, character_slug: str) -> List[NormalizedImportRecord]:
        records: List[NormalizedImportRecord] = []
        for item in raw_payload:
            normalized_not = NotationEngine.normalize_string(item.get("input", ""))
            records.append(
                NormalizedImportRecord(
                    character_slug=item.get("character_slug", character_slug),
                    stable_source_id=item.get("id"),
                    move_name=item.get("name"),
                    original_notation=item.get("input", ""),
                    normalized_notation=normalized_not,
                    startup_frames=item.get("startup_frames"),
                    startup_raw=item.get("startup_raw"),
                    block_advantage=item.get("block_advantage"),
                    block_advantage_raw=item.get("block_advantage_raw"),
                    hit_advantage=item.get("hit_advantage"),
                    hit_advantage_raw=item.get("hit_advantage_raw"),
                    ch_advantage=item.get("ch_advantage"),
                    ch_advantage_raw=item.get("ch_advantage_raw"),
                    damage=item.get("damage"),
                    damage_raw=item.get("damage_raw"),
                    hit_level=item.get("hit_level"),
                    stance_context=item.get("stance_context"),
                    properties=item.get("properties", []),
                    patch_version=item.get("patch_version", "3.00.02"),
                    source_reference_url="data/fixtures/sample_moves.json"
                )
            )
        return records

    def run_import(self, character_slug: str, fixture_path: str = "data/fixtures/sample_moves.json") -> BatchImportReport:
        report = BatchImportReport(
            source_name=self.source_name,
            source_url=fixture_path,
            patch_version="3.00.02"
        )
        try:
            raw = self.fetch_raw_data(character_slug, fixture_path=fixture_path)
            raw_path = self.preserve_raw_payload(character_slug, raw)
            report.raw_payload_path = raw_path
            records = self.parse_payload(raw, character_slug)
            report.total_records = len(records)
            report.imported_records = records
            report.successful_records = len(records)
        except Exception as e:
            report.failed_records = report.total_records
            report.errors.append({"error": str(e), "character": character_slug})
        return report
