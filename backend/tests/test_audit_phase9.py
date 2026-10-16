"""
Phase 9 Forensic Audit & Integrity Regression Tests.
Verifies character roster completeness, frame-data nullability semantics,
stage blueprint assets, DataValidator health score (100.0/100), and UI deduplication.
"""

import os
import pytest
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.stage import Stage
from backend.app.models.combo_route import ComboRoute
from backend.app.services.data_validator import DataValidator


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_character_roster_completeness(db_session: Session):
    """Verify that exactly 43 canonical Tekken 8 characters exist in the database."""
    total_characters = db_session.query(Character).count()
    assert total_characters == 43, f"Expected exactly 43 characters, found {total_characters}"


def test_move_count_and_verification_status(db_session: Session):
    """Verify that all moves in the production database have VERIFIED status."""
    total_moves = db_session.query(Move).count()
    assert total_moves >= 247, f"Expected at least 247 moves, found {total_moves}"

    unverified = db_session.query(Move).filter(Move.verification_status != "VERIFIED").count()
    assert unverified == 0, f"Found {unverified} unverified moves in database"


def test_null_block_advantage_semantic_validity(db_session: Session):
    """
    Verify that moves with NULL block_advantage are exclusively Stance Transitions
    (hit_level='s') or Command Throws (hit_level='t'), where block frame data is
    domain-logically NOT_APPLICABLE rather than a missing data defect.
    """
    null_block_moves = db_session.query(Move).filter(Move.block_advantage.is_(None)).all()
    assert len(null_block_moves) == 43, f"Expected exactly 43 null-block moves, found {len(null_block_moves)}"

    for m in null_block_moves:
        assert m.hit_level in ("s", "t"), (
            f"Move #{m.id} '{m.name}' has null block_advantage but hit_level='{m.hit_level}'. "
            f"Only stance transitions ('s') and command throws ('t') may have null block."
        )


def test_null_startup_frames_semantic_validity(db_session: Session):
    """
    Verify that all 32 moves with NULL startup_frames are pure Stance Transitions (hit_level='s')
    and possess an explanatory raw entry (e.g. 'N/A' or 'N/A (i20)').
    """
    null_startup_moves = db_session.query(Move).filter(Move.startup_frames.is_(None)).all()
    assert len(null_startup_moves) == 32, f"Expected exactly 32 null-startup moves, found {len(null_startup_moves)}"

    for m in null_startup_moves:
        assert m.hit_level == "s", f"Move #{m.id} has null startup but hit_level='{m.hit_level}'"
        assert m.startup_raw is not None, f"Move #{m.id} has null startup and missing startup_raw"


def test_stage_assets_presence_and_blueprints(db_session: Session):
    """Verify that all 16 stages exist and their asset files exist on disk without 404s."""
    stages = db_session.query(Stage).all()
    assert len(stages) == 16, f"Expected 16 stages, found {len(stages)}"

    for s in stages:
        assert s.image_url, f"Stage {s.slug} is missing image_url"
        rel_path = s.image_url.lstrip("/")
        full_path = os.path.join("frontend", rel_path)
        assert os.path.exists(full_path), f"Stage image asset not found on disk: {full_path}"

    # Verify dedicated tactical blueprints for stages 11-16
    svg_stages = ["urban-square-evening", "arena-underground", "elegant-palace", 
                  "descent-into-subconscious", "secluded-training-ground", "genmaji-temple"]
    for slug in svg_stages:
        stg = db_session.query(Stage).filter_by(slug=slug).first()
        assert stg is not None, f"Stage {slug} not found in DB"
        assert stg.image_url.endswith(".svg"), f"Stage {slug} expected .svg blueprint, got {stg.image_url}"


def test_datavalidator_audit_clean_slate(db_session: Session):
    """Verify that DataValidator.audit_entire_database yields 100% health score and 0 issues."""
    report = DataValidator.audit_entire_database(db_session)
    assert report.is_healthy is True
    assert report.health_score == 100.0
    assert report.critical_issues_count == 0
    assert report.error_issues_count == 0
    assert report.warning_issues_count == 0
    assert len(report.issues) == 0


def test_frontend_ui_deduplication():
    """Verify that obsolete components (.left-rail, .right-sidebar-panel) are purged from index.html."""
    html_path = os.path.join("frontend", "index.html")
    assert os.path.exists(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "class=\"left-rail\"" not in html_content
    assert "class=\"right-sidebar-panel\"" not in html_content
    assert "sidebar-quick-fighters" not in html_content
