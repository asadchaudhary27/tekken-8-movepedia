import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.database.session import SessionLocal
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.stage import Stage
from backend.app.models.verification import VerificationRecord
from backend.app.services.data_validator import DataValidator
from backend.app.services.admin_data_service import AdminDataService


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_headers():
    return {
        "X-Admin-Key": settings.ADMIN_SECRET_KEY,
        "X-Admin-User": "Lead Lab Architect",
    }



# ==============================================================================
# 1. MOVE VALIDATION TESTS (Missing values, bounds, syntax)
# ==============================================================================

def test_validate_move_valid():
    data = {
        "character_slug": "jin",
        "normalized_notation": "d/f+2",
        "startup_frames": 15,
        "startup_raw": "15",
        "block_advantage": -7,
        "hit_advantage": 4,
        "damage": 17,
        "hit_level": "m",
        "verification_status": "VERIFIED",
    }
    res = DataValidator.validate_move(data)
    assert res.is_valid is True
    assert res.errors_count == 0


def test_validate_move_rejects_negative_and_zero_startup():
    # Negative startup
    neg_data = {
        "normalized_notation": "1, 2",
        "startup_frames": -5,
    }
    res_neg = DataValidator.validate_move(neg_data)
    assert res_neg.is_valid is False
    assert any(i.rule == "STARTUP_FRAMES_POSITIVE" for i in res_neg.issues)

    # Zero startup (null converted to 0 defect)
    zero_data = {
        "normalized_notation": "1, 2",
        "startup_frames": 0,
    }
    res_zero = DataValidator.validate_move(zero_data)
    assert res_zero.is_valid is False
    assert any(i.rule == "STARTUP_FRAMES_POSITIVE" for i in res_zero.issues)


def test_validate_move_missing_value_semantics():
    # Valid missing value: stance or unrecorded startup with NULL startup_frames
    data = {
        "normalized_notation": "ZEN",
        "startup_frames": None,
        "startup_raw": "N/A",
        "block_advantage": None,
        "block_advantage_raw": "N/A",
        "damage": 0,
        "hit_level": "s",
    }
    res = DataValidator.validate_move(data)
    # Stance with damage 0 and null frames is valid (no critical errors)
    assert res.is_valid is True
    assert res.errors_count == 0


def test_validate_move_rejects_negative_damage():
    data = {
        "normalized_notation": "d/f+1",
        "damage": -15,
    }
    res = DataValidator.validate_move(data)
    assert res.is_valid is False
    assert any(i.rule == "DAMAGE_NON_NEGATIVE" for i in res.issues)


def test_validate_move_detects_corrupt_syntax():
    data = {
        "normalized_notation": "d/f+2<script>alert(1)</script>",
        "startup_frames": 15,
    }
    res = DataValidator.validate_move(data)
    assert res.is_valid is False
    assert any(i.rule == "INVALID_NOTATION_SYNTAX" for i in res.issues)


def test_validate_move_detects_duplicate_notation(db_session: Session):
    jin = db_session.query(Character).filter_by(slug="jin").first()
    assert jin is not None
    first_move = db_session.query(Move).filter_by(character_id=jin.id).first()
    assert first_move is not None

    dup_data = {
        "character_id": jin.id,
        "normalized_notation": first_move.normalized_notation,
        "startup_frames": 10,
    }
    res = DataValidator.validate_move(dup_data, db=db_session)
    assert res.is_valid is False
    assert any(i.rule == "DUPLICATE_MOVE_NOTATION" for i in res.issues)


# ==============================================================================
# 2. COMBO VALIDATION TESTS (Starter ownership, stage hazard invariants)
# ==============================================================================

def test_validate_combo_valid():
    combo_data = {
        "title": "Standard Bread and Butter",
        "notation_sequence": "d/f+2 > 4 > b+2,1 > ender",
        "total_damage": 68,
        "hit_count": 8,
        "difficulty": "MEDIUM",
        "combo_type": "MIDSCREEN",
    }
    res = DataValidator.validate_combo(combo_data)
    assert res.is_valid is True
    assert res.errors_count == 0


def test_validate_combo_rejects_invalid_damage_and_hits():
    # Negative damage
    res_dmg = DataValidator.validate_combo({
        "title": "Invalid Combo",
        "notation_sequence": "1 > 2",
        "total_damage": -50,
        "hit_count": 2,
    })
    assert res_dmg.is_valid is False
    assert any(i.rule == "COMBO_DAMAGE_POSITIVE" for i in res_dmg.issues)

    # 0 hits
    res_hits = DataValidator.validate_combo({
        "title": "Invalid Combo",
        "notation_sequence": "1 > 2",
        "total_damage": 50,
        "hit_count": 0,
    })
    assert res_hits.is_valid is False
    assert any(i.rule == "COMBO_HIT_COUNT_POSITIVE" for i in res_hits.issues)


def test_validate_combo_detects_starter_character_mismatch(db_session: Session):
    jin = db_session.query(Character).filter_by(slug="jin").first()
    kazuya = db_session.query(Character).filter_by(slug="kazuya").first()
    assert jin is not None and kazuya is not None

    kazuya_move = db_session.query(Move).filter_by(character_id=kazuya.id).first()
    assert kazuya_move is not None

    # Mismatch: Jin combo referencing a Kazuya move as its launcher
    mismatched_combo = {
        "character_id": jin.id,
        "title": "Impossible Jin Combo with Kazuya Move",
        "notation_sequence": "starter > route",
        "total_damage": 65,
        "hit_count": 5,
        "starter_move_id": kazuya_move.id,
    }
    res = DataValidator.validate_combo(mismatched_combo, db=db_session)
    assert res.is_valid is False
    assert any(i.rule == "STARTER_CHARACTER_MISMATCH" for i in res.issues)


def test_validate_combo_detects_stage_hazard_conflicts(db_session: Session):
    # Find an infinite stage without walls (e.g. colosseum or create/check stage with has_walls=False)
    infinite_stage = db_session.query(Stage).filter_by(has_walls=False).first()
    if not infinite_stage:
        # Create a transient test stage check
        test_stage_data = {
            "slug": "infinite-test-arena",
            "name": "Infinite Void",
            "has_walls": False,
        }
        res_stage = DataValidator.validate_stage({
            "slug": "infinite-void",
            "name": "Infinite Void",
            "has_walls": False,
            "wall_break": True,  # Conflict!
        })
        assert res_stage.is_valid is False
        assert any(i.rule == "INFINITE_STAGE_HAS_WALL_HAZARDS" for i in res_stage.issues)
    else:
        # Combo on infinite stage requiring wall break
        conflicting_combo = {
            "title": "Wall Break on Infinite Stage",
            "notation_sequence": "starter > wall break",
            "total_damage": 70,
            "hit_count": 6,
            "combo_type": "WALL_BREAK",
            "stage_id": infinite_stage.id,
            "uses_wall": True,
        }
        res = DataValidator.validate_combo(conflicting_combo, db=db_session)
        assert res.is_valid is False
        assert any(i.rule == "STAGE_HAZARD_CONFLICT" for i in res.issues)


def test_validate_combo_rejects_self_referential_alternative():
    combo_data = {
        "id": 42,
        "title": "Recursive Combo",
        "notation_sequence": "1 > 2",
        "total_damage": 50,
        "hit_count": 2,
        "easier_alternative_id": 42,
    }
    res = DataValidator.validate_combo(combo_data)
    assert res.is_valid is False
    assert any(i.rule == "SELF_REFERENTIAL_ALTERNATIVE" for i in res.issues)


# ==============================================================================
# 3. DATABASE INTEGRITY AUDIT SUITE
# ==============================================================================

def test_audit_entire_database(db_session: Session):
    report = DataValidator.audit_entire_database(db_session)
    assert report.total_characters >= 4
    assert report.total_moves > 0
    assert report.total_combos > 0
    assert report.total_stages > 0
    assert report.health_score > 70.0
    assert report.missing_value_summary["total_moves_scanned"] == report.total_moves
    assert len(report.recommendations) > 0


# ==============================================================================
# 4. ADMIN API AUDIT & VALIDATION ENDPOINTS
# ==============================================================================

def test_api_database_integrity_audit(client: TestClient, admin_headers: dict):
    response = client.post("/api/v1/admin/audit/integrity", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "health_score" in data
    assert "total_characters" in data
    assert "total_moves" in data
    assert "recommendations" in data


def test_api_validate_move_endpoint(client: TestClient, admin_headers: dict):
    # Valid move check
    response = client.post(
        "/api/v1/admin/validate/move",
        json={
            "normalized_notation": "f,F+2",
            "startup_frames": 13,
            "damage": 22,
            "block_advantage": -11,
            "hit_level": "m",
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True

    # Invalid move check (negative startup)
    response_invalid = client.post(
        "/api/v1/admin/validate/move",
        json={
            "normalized_notation": "f,F+2",
            "startup_frames": -10,
        },
        headers=admin_headers,
    )
    assert response_invalid.status_code == 200
    inv_data = response_invalid.json()
    assert inv_data["is_valid"] is False
    assert inv_data["errors_count"] >= 1


def test_api_validate_combo_endpoint(client: TestClient, admin_headers: dict):
    # Valid combo
    response = client.post(
        "/api/v1/admin/validate/combo",
        json={
            "title": "API Test Route",
            "notation_sequence": "launcher > filler > ender",
            "total_damage": 65,
            "hit_count": 7,
            "difficulty": "EASY",
            "combo_type": "MIDSCREEN",
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True


# ==============================================================================
# 5. SAFE DATA IMPORT ENGINE (Dry run, validation, verified protection)
# ==============================================================================

def test_import_preview_with_semantic_validation(db_session: Session):
    jin = db_session.query(Character).filter_by(slug="jin").first()
    assert jin is not None

    invalid_payload = f"""[
        {{
            "character_id": {jin.id},
            "normalized_notation": "d/f+3_invalid",
            "startup_frames": -8,
            "damage": -20
        }}
    ]"""

    preview = AdminDataService.preview_import(
        db=db_session,
        entity_type="MOVES",
        raw_content=invalid_payload,
        format_type="JSON",
    )

    assert preview.total_rows == 1
    assert preview.error_rows_count >= 1
    assert preview.is_importable is False
    assert any(i.field == "startup_frames" for i in preview.issues)


def test_execute_import_atomic_rollback_on_critical_validation_error(db_session: Session):
    jin = db_session.query(Character).filter_by(slug="jin").first()
    assert jin is not None

    # Payload with invalid negative startup frames that violates DataValidator
    invalid_rows = [
        {
            "character_id": jin.id,
            "normalized_notation": "qcf+1_rollback_test",
            "startup_frames": -14,
            "damage": 25,
            "verification_status": "UNVERIFIED",
        }
    ]

    summary = AdminDataService.execute_import(
        db=db_session,
        entity_type="MOVES",
        rows=invalid_rows,
        user="test_admin",
    )

    assert summary.success is False
    assert summary.rollback_occurred is True
    assert "validation failed" in summary.message.lower() or "startup" in summary.message.lower()

    # Verify move was NOT persisted
    test_move = db_session.query(Move).filter_by(
        character_id=jin.id, normalized_notation="qcf+1_rollback_test"
    ).first()
    assert test_move is None
