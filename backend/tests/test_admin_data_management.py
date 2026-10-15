import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.stage import Stage
from backend.app.models.source import DataSource
from backend.app.models.verification import VerificationRecord
from backend.app.models.conflict import DataConflict
from backend.app.services.admin_data_service import AdminDataService
from backend.app.schemas.admin import (
    MoveAdminCreateUpdate,
    ComboAdminCreateUpdate,
    StageMechanicsAdminUpdate,
)

ADMIN_HEADERS = {
    "X-Admin-Key": settings.ADMIN_SECRET_KEY,
    "X-Admin-User": "Lead Lab Architect",
}


def test_admin_permissions_unauthorized_vs_authorized(client: TestClient):
    """
    Test permission barrier: non-admin requests must receive 401 Unauthorized.
    """
    # 1. No credentials
    resp = client.get("/api/v1/admin/dashboard")
    assert resp.status_code == 401
    assert "denied" in resp.json()["detail"].lower() or "required" in resp.json()["detail"].lower()

    # 2. Invalid credentials
    resp = client.get("/api/v1/admin/dashboard", headers={"X-Admin-Key": "wrong-secret-key"})
    assert resp.status_code == 401

    # 3. Valid credentials
    resp = client.get("/api/v1/admin/dashboard", headers=ADMIN_HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_characters" in data
    assert data["total_characters"] == 43


def test_admin_quality_dashboard_metrics(client: TestClient):
    """
    Test Quality Dashboard KPI metrics, audit alerts, and differentiation of missing data states.
    """
    resp = client.get("/api/v1/admin/dashboard", headers=ADMIN_HEADERS)
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_characters"] == 43
    assert data["total_stages"] >= 10
    assert data["total_moves"] > 0
    assert data["total_combos"] > 0
    assert "status_distribution" in data

    # Differentiates status values without converting missing data to zero/false
    dist = data["status_distribution"]
    assert "VERIFIED" in dist
    assert "UNVERIFIED" in dist
    assert "UNKNOWN" in dist
    assert "NOT_PROVIDED" in dist
    assert "CONFIRMED_ABSENT" in dist

    # Verify audit issues structure
    assert "audit_issues" in data
    assert isinstance(data["audit_issues"], list)


def test_add_and_edit_move_with_non_destructive_audit_trail(test_db: Session):
    """
    Test creating and modifying a move while preserving historical changes in VerificationRecord.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    assert jin is not None

    # 1. Create move
    create_dto = MoveAdminCreateUpdate(
        character_id=jin.id,
        name="Test Audit Uppercut",
        normalized_notation="df+1+2",
        startup_frames=15,
        block_advantage=-12,
        damage=22,
        hit_level="m",
        verification_status="UNVERIFIED",
        reason_for_change="Initial community discovery",
    )
    move = AdminDataService.save_move(test_db, create_dto, user="TestAdmin")
    assert move.id is not None
    assert move.block_advantage == -12

    # Check creation audit record
    rec1 = (
        test_db.query(VerificationRecord)
        .filter_by(entity_type="MOVE", entity_id=move.id, field_name="CREATE_RECORD")
        .first()
    )
    assert rec1 is not None
    assert rec1.verified_by == "TestAdmin"

    # 2. Edit move to correct block advantage to -10
    edit_dto = MoveAdminCreateUpdate(
        character_id=jin.id,
        name="Test Audit Uppercut",
        normalized_notation="df+1+2",
        startup_frames=15,
        block_advantage=-10,  # Changed from -12 to -10
        damage=22,
        hit_level="m",
        verification_status="VERIFIED",
        reason_for_change="Lab frame test verified -10 on block",
    )
    updated_move = AdminDataService.save_move(test_db, edit_dto, user="TestAdmin2")
    assert updated_move.block_advantage == -10
    assert updated_move.verification_status == "VERIFIED"

    # Check that the change was recorded non-destructively in audit trail
    rec2 = (
        test_db.query(VerificationRecord)
        .filter_by(entity_type="MOVE", entity_id=move.id, field_name="block_advantage")
        .first()
    )
    assert rec2 is not None
    assert rec2.old_value == "-12"
    assert rec2.new_value == "-10"
    assert rec2.verified_by == "TestAdmin2"
    assert "Lab frame test" in rec2.evidence_notes

    # Clean up test move and its audit records
    test_db.query(VerificationRecord).filter_by(entity_id=move.id).delete()
    test_db.delete(updated_move)
    test_db.commit()


def test_update_verification_status_and_audit_history(test_db: Session):
    """
    Test changing status to VERIFIED, CONFLICTING, UNAVAILABLE with full audit trail.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    move = test_db.query(Move).filter_by(character_id=jin.id).first()
    assert move is not None

    orig_status = move.verification_status

    # 1. Update status to CONFLICTING
    res1 = AdminDataService.update_verification_status(
        db=test_db,
        entity_type="MOVE",
        entity_id=move.id,
        new_status="CONFLICTING",
        evidence="Frame advantage disputes between Namco sheet and practice lab",
        user="QualityOfficer",
    )
    assert res1["new_status"] == "CONFLICTING"

    # 2. Update status to VERIFIED
    res2 = AdminDataService.update_verification_status(
        db=test_db,
        entity_type="MOVE",
        entity_id=move.id,
        new_status="VERIFIED",
        evidence="Resolved via high-speed 60fps frame count recording",
        user="QualityOfficer",
    )
    assert res2["new_status"] == "VERIFIED"

    # Verify both records exist in history
    records = (
        test_db.query(VerificationRecord)
        .filter_by(entity_type="MOVE", entity_id=move.id, field_name="verification_status")
        .order_by(VerificationRecord.id.desc())
        .all()
    )
    assert len(records) >= 2
    assert records[0].new_value == "VERIFIED"
    assert records[1].new_value == "CONFLICTING"

    # Restore original status
    move.verification_status = orig_status
    test_db.commit()


def test_csv_and_json_import_preview_validation_failures(test_db: Session):
    """
    Test import preview detects validation errors (missing fields, invalid character).
    """
    bad_json = """
    [
        {"name": "Missing Char Move", "normalized_notation": "1,2"},
        {"character_id": 99999, "name": "Nonexistent Char", "normalized_notation": "df+2"},
        {"character_id": 1, "name": "Missing Notation Move"}
    ]
    """
    preview = AdminDataService.preview_import(
        db=test_db,
        entity_type="MOVES",
        raw_content=bad_json,
        format_type="JSON",
    )

    assert preview.total_rows == 3
    assert preview.error_rows_count >= 2
    assert preview.is_importable is False
    assert len(preview.issues) >= 2


def test_import_duplicate_detection(test_db: Session):
    """
    Test duplicate detection for moves already existing in database.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    exist_move = test_db.query(Move).filter_by(character_id=jin.id).first()

    dup_json = f"""
    [
        {{
            "character_id": {jin.id},
            "name": "{exist_move.name}",
            "normalized_notation": "{exist_move.normalized_notation}",
            "startup_frames": {exist_move.startup_frames or 10},
            "block_advantage": {exist_move.block_advantage or -1},
            "verification_status": "VERIFIED"
        }}
    ]
    """
    preview = AdminDataService.preview_import(
        db=test_db,
        entity_type="MOVES",
        raw_content=dup_json,
        format_type="JSON",
    )

    assert preview.total_rows == 1
    assert preview.duplicate_count == 1


def test_protection_verified_records_not_silently_overwritten(test_db: Session):
    """
    CRITICAL RULE: Never silently overwrite verified data with an unverified import.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    # Find a verified move
    verified_move = (
        test_db.query(Move)
        .filter_by(character_id=jin.id, verification_status="VERIFIED")
        .first()
    )
    assert verified_move is not None

    orig_block = verified_move.block_advantage

    # Unverified import attempting to change block advantage
    unverified_payload = [
        {
            "character_id": jin.id,
            "name": verified_move.name,
            "normalized_notation": verified_move.normalized_notation,
            "startup_frames": verified_move.startup_frames,
            "block_advantage": (orig_block or 0) - 5,
            "verification_status": "UNVERIFIED",
        }
    ]

    # Preview must flag protection warning
    raw_json = f"""
    [{{
        "character_id": {jin.id},
        "name": "{verified_move.name}",
        "normalized_notation": "{verified_move.normalized_notation}",
        "startup_frames": {verified_move.startup_frames or 10},
        "block_advantage": -99,
        "verification_status": "UNVERIFIED"
    }}]
    """
    preview = AdminDataService.preview_import(
        db=test_db,
        entity_type="MOVES",
        raw_content=raw_json,
        format_type="JSON",
    )
    assert preview.verified_protection_count >= 1

    # Execute import with allow_override_verified=False (default safe mode)
    summary = AdminDataService.execute_import(
        db=test_db,
        entity_type="MOVES",
        rows=unverified_payload,
        user="SafeImporter",
        allow_override_verified=False,
    )
    assert summary.records_updated == 0
    assert summary.records_skipped == 1
    assert summary.conflicts_logged >= 1

    # Verify original data was preserved unchanged
    test_db.refresh(verified_move)
    assert verified_move.block_advantage == orig_block
    assert verified_move.verification_status == "VERIFIED"

    # Clean up logged conflict
    test_db.query(DataConflict).filter_by(move_id=verified_move.id).delete()
    test_db.commit()


def test_transaction_safe_import_atomic_rollback(test_db: Session):
    """
    Test atomic transaction rollback: if an invalid row triggers failure,
    no rows are committed to database.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    count_before = test_db.query(Move).count()

    # Batch with 1 good row and 1 fatally bad row (missing notation)
    rows = [
        {
            "character_id": jin.id,
            "name": "Valid Candidate",
            "normalized_notation": "f+1+4_test_rollback",
            "startup_frames": 14,
            "verification_status": "UNVERIFIED",
        },
        {
            "character_id": jin.id,
            # Missing notation -> triggers ValueError in loop
            "name": "Bad Candidate Without Notation",
        },
    ]

    summary = AdminDataService.execute_import(
        db=test_db,
        entity_type="MOVES",
        rows=rows,
        user="RollbackTester",
    )

    assert summary.success is False
    assert summary.rollback_occurred is True
    assert summary.records_created == 0

    # Ensure nothing was committed
    count_after = test_db.query(Move).count()
    assert count_after == count_before


def test_data_changes_across_patches_and_provenance(test_db: Session):
    """
    Test patch version tracking and detection of outdated patch records.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()

    # Create a move on an older patch (1.05.00)
    legacy_move = Move(
        character_id=jin.id,
        name="Legacy Season 1 Move",
        normalized_notation="b+3+4_legacy",
        original_notation="b+3+4",
        startup_frames=18,
        block_advantage=-14,
        verification_status="VERIFIED",
    )
    test_db.add(legacy_move)
    test_db.commit()
    test_db.refresh(legacy_move)

    AdminDataService.log_audit_trail(
        db=test_db,
        entity_type="MOVE",
        entity_id=legacy_move.id,
        field_name="PATCH_VERSION",
        old_val=None,
        new_val="1.05.00",
        user="PatchArchivist",
        method="HISTORICAL_ARCHIVE",
        result="VERIFIED",
        notes="Documented on initial launch patch 1.05.00",
        patch_version="1.05.00",
    )
    test_db.commit()

    verif = (
        test_db.query(VerificationRecord)
        .filter_by(entity_id=legacy_move.id, patch_version="1.05.00")
        .first()
    )
    assert verif is not None
    assert verif.patch_version == "1.05.00"

    # Cleanup
    test_db.query(VerificationRecord).filter_by(entity_id=legacy_move.id).delete()
    test_db.delete(legacy_move)
    test_db.commit()


def test_export_dataset_csv_and_json(client: TestClient):
    """
    Test export endpoint returns valid CSV and JSON representations.
    """
    # 1. JSON Export
    resp_json = client.get("/api/v1/admin/export/moves?format=JSON", headers=ADMIN_HEADERS)
    assert resp_json.status_code == 200
    assert "application/json" in resp_json.headers["content-type"]
    data = resp_json.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "normalized_notation" in data[0]

    # 2. CSV Export
    resp_csv = client.get("/api/v1/admin/export/moves?format=CSV", headers=ADMIN_HEADERS)
    assert resp_csv.status_code == 200
    assert "text/csv" in resp_csv.headers["content-type"]
    csv_text = resp_csv.text
    assert "normalized_notation" in csv_text
    assert "\n" in csv_text


def test_data_sources_licensing_and_attribution(client: TestClient):
    """
    Test data sources list preserves licensing and attribution information.
    """
    resp = client.get("/api/v1/admin/sources", headers=ADMIN_HEADERS)
    assert resp.status_code == 200
    sources = resp.json()
    assert len(sources) >= 5

    wavu = next((s for s in sources if "wavu" in s["name"].lower()), None)
    assert wavu is not None
    assert "CC" in wavu["license_type"]
    assert wavu["attribution_text"] is not None

    tekken_docs = next((s for s in sources if "tekkendocs" in s["name"].lower()), None)
    assert tekken_docs is not None
    assert tekken_docs["license_type"] is not None
