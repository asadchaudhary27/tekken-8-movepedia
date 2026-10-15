"""
Abstract Base Adapter for Data Fetching & Extraction.
Enforces source identification, rate limiting, raw payload preservation,
and normalized record generation without exposing credentials.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import json
import os
from pydantic import BaseModel


class NormalizedImportRecord(BaseModel):
    """Standardized intermediate representation for imported Tekken moves."""
    character_slug: str
    stable_source_id: Optional[str] = None
    move_name: Optional[str] = None
    original_notation: str
    normalized_notation: str
    startup_frames: Optional[int] = None
    startup_raw: Optional[str] = None
    block_advantage: Optional[int] = None
    block_advantage_raw: Optional[str] = None
    hit_advantage: Optional[int] = None
    hit_advantage_raw: Optional[str] = None
    ch_advantage: Optional[int] = None
    ch_advantage_raw: Optional[str] = None
    damage: Optional[int] = None
    damage_raw: Optional[str] = None
    hit_level: Optional[str] = None
    stance_context: Optional[str] = None
    properties: List[str] = []
    patch_version: str = "unknown"
    source_reference_url: Optional[str] = None


class BatchImportReport(BaseModel):
    source_name: str
    source_url: str
    patch_version: str
    total_records: int = 0
    successful_records: int = 0
    failed_records: int = 0
    skipped_duplicates: int = 0
    raw_payload_path: Optional[str] = None
    errors: List[Dict[str, Any]] = []
    imported_records: List[NormalizedImportRecord] = []


class BaseSourceAdapter(ABC):
    """Abstract interface all source adapters must implement."""

    def __init__(self, raw_storage_dir: str = "data/raw"):
        self.raw_storage_dir = raw_storage_dir
        os.makedirs(self.raw_storage_dir, exist_ok=True)

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Canonical machine-readable source identifier."""
        pass

    @property
    @abstractmethod
    def approval_status(self) -> str:
        """Approval status: APPROVED, APPROVED_WITH_RESTRICTIONS, RESEARCH_ONLY."""
        pass

    @property
    @abstractmethod
    def rate_limit_delay_seconds(self) -> float:
        """Minimum delay between subsequent automated requests."""
        pass

    @abstractmethod
    def fetch_raw_data(self, character_slug: str, **kwargs) -> Any:
        """Fetches raw payload from source."""
        pass

    @abstractmethod
    def parse_payload(self, raw_payload: Any, character_slug: str) -> List[NormalizedImportRecord]:
        """Parses raw payload into normalized records."""
        pass

    def preserve_raw_payload(self, character_slug: str, raw_payload: Any) -> str:
        """Saves unmodified payload to data/raw/<source>_<char>_<timestamp>.json."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{self.source_name}_{character_slug}_{timestamp}.json"
        filepath = os.path.join(self.raw_storage_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            if isinstance(raw_payload, (dict, list)):
                json.dump(raw_payload, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(raw_payload))
        return filepath
