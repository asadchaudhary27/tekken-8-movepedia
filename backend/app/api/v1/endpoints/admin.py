from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.core.admin_auth import verify_admin_token
from backend.app.models.source import DataSource
from backend.app.models.patch import GamePatch
from backend.app.models.verification import VerificationRecord
from backend.app.models.move import Move
from backend.app.models.character import Character
from backend.app.services.admin_data_service import AdminDataService
from backend.app.schemas.admin import (
    QualityDashboardStats,
    VerificationRecordRead,
    StatusUpdateRequest,
    MoveAdminCreateUpdate,
    ComboAdminCreateUpdate,
    StageMechanicsAdminUpdate,
    DataSourceCreateUpdate,
    GamePatchCreateUpdate,
    ImportPreviewRequest,
    ImportPreviewResponse,
    ImportExecuteRequest,
    ImportSummaryResponse,
    DatabaseAuditReport,
    ValidationResult,
    MoveValidationRequest,
    ComboValidationRequest,
)
from backend.app.services.data_validator import DataValidator

router = APIRouter()



@router.get("/dashboard", response_model=QualityDashboardStats)
def get_admin_quality_dashboard(
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Returns data quality dashboard metrics, missing frame data, incomplete mechanics,
    unverified punishes, conflicting records, and audit issues.
    """
    return AdminDataService.get_quality_dashboard(db)


@router.get("/sources")
def list_data_sources(
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Lists external data providers, their approval status, license type, and attribution text.
    """
    sources = db.query(DataSource).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "base_url": s.base_url,
            "license_type": s.license_type,
            "attribution_text": s.attribution_text,
            "license_url": s.license_url,
            "approval_status": s.approval_status,
            "rate_limit_policy": s.rate_limit_policy,
            "is_active": s.is_active,
        }
        for s in sources
    ]


@router.post("/sources")
def create_or_update_data_source(
    payload: DataSourceCreateUpdate,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Adds or updates a data source and its attribution licensing policy.
    """
    src = db.query(DataSource).filter_by(name=payload.name).first()
    if src:
        src.base_url = payload.base_url
        src.license_type = payload.license_type
        src.attribution_text = payload.attribution_text
        src.license_url = payload.license_url
        src.approval_status = payload.approval_status
        src.rate_limit_policy = payload.rate_limit_policy
        src.is_active = payload.is_active
    else:
        src = DataSource(
            name=payload.name,
            base_url=payload.base_url,
            license_type=payload.license_type,
            attribution_text=payload.attribution_text,
            license_url=payload.license_url,
            approval_status=payload.approval_status,
            rate_limit_policy=payload.rate_limit_policy,
            is_active=payload.is_active,
        )
        db.add(src)

    db.commit()
    db.refresh(src)
    return {"message": "Data source saved successfully", "source_id": src.id, "name": src.name}


@router.get("/patches")
def list_game_patches(
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Lists recorded Tekken 8 patch versions.
    """
    patches = db.query(GamePatch).all()
    return [
        {
            "id": p.id,
            "version_number": p.version_number,
            "release_date": str(p.release_date) if p.release_date else None,
            "notes": p.notes,
            "is_current": p.is_current,
        }
        for p in patches
    ]


@router.post("/patches")
def create_game_patch(
    payload: GamePatchCreateUpdate,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Registers a new patch version and optionally sets it as current.
    """
    if payload.is_current:
        # Mark all others as not current
        db.query(GamePatch).update({GamePatch.is_current: False})

    patch = db.query(GamePatch).filter_by(version_number=payload.version_number).first()
    if patch:
        patch.notes = payload.notes
        patch.is_current = payload.is_current
    else:
        patch = GamePatch(
            version_number=payload.version_number,
            notes=payload.notes,
            is_current=payload.is_current,
        )
        db.add(patch)

    db.commit()
    db.refresh(patch)
    return {"message": "Game patch saved", "version": patch.version_number, "is_current": patch.is_current}


@router.get("/history", response_model=List[VerificationRecordRead])
def get_verification_history(
    entity_type: Optional[str] = Query(None, description="Filter by MOVE, COMBO, MATCHUP_NOTE, STAGE"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Returns audit trail logs showing non-destructive history of all changes and verifications.
    """
    q = db.query(VerificationRecord)
    if entity_type:
        q = q.filter(VerificationRecord.entity_type == entity_type.upper())
    records = q.order_by(VerificationRecord.verified_at.desc()).limit(limit).all()
    return records


@router.post("/verification-status")
def update_verification_status(
    payload: StatusUpdateRequest,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Marks a record as VERIFIED, UNVERIFIED, CONFLICTING, UNAVAILABLE, or CONFIRMED_ABSENT
    while appending to the non-destructive audit trail.
    """
    try:
        res = AdminDataService.update_verification_status(
            db=db,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            new_status=payload.new_status,
            evidence=payload.evidence_notes,
            user=admin_user,
            source_url=payload.source_url,
            patch_version=payload.patch_version,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/moves")
def add_or_edit_move(
    payload: MoveAdminCreateUpdate,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Adds or updates a character move with audit logging.
    """
    try:
        move = AdminDataService.save_move(db=db, data=payload, user=admin_user)
        return {
            "message": "Move saved successfully",
            "move_id": move.id,
            "name": move.name,
            "normalized_notation": move.normalized_notation,
            "startup_frames": move.startup_frames,
            "block_advantage": move.block_advantage,
            "verification_status": move.verification_status,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/combos")
def add_or_edit_combo(
    payload: ComboAdminCreateUpdate,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Adds or updates a combo route with audit logging.
    """
    try:
        combo = AdminDataService.save_combo(db=db, data=payload, user=admin_user)
        return {
            "message": "Combo route saved successfully",
            "combo_id": combo.id,
            "title": combo.title,
            "total_damage": combo.total_damage,
            "verification_status": combo.verification_status,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/stage-mechanics/{stage_id}")
def update_stage_mechanics(
    stage_id: int,
    payload: StageMechanicsAdminUpdate,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Adds or updates stage hazard mechanics, boundaries, and layout properties.
    """
    try:
        stage = AdminDataService.save_stage_mechanics(
            db=db, stage_id=stage_id, data=payload, user=admin_user
        )
        return {
            "message": "Stage mechanics updated successfully",
            "stage_id": stage.id,
            "name": stage.name,
            "wall_break": stage.wall_break,
            "floor_break": stage.floor_break,
            "balcony_break": stage.balcony_break,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/import/preview", response_model=ImportPreviewResponse)
def preview_import_data(
    payload: ImportPreviewRequest,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Parses and validates CSV/JSON data, detects duplicates, conflicts, and warns
    if incoming unverified data risks overwriting verified records.
    """
    try:
        res = AdminDataService.preview_import(
            db=db,
            entity_type=payload.entity_type,
            raw_content=payload.raw_content,
            format_type=payload.format,
            source_name=payload.source_name,
            patch_version=payload.patch_version,
            field_mapping=payload.field_mapping,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/import/execute", response_model=ImportSummaryResponse)
def execute_import_data(
    payload: ImportExecuteRequest,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Executes transaction-safe import. Rolls back on error.
    Protects verified records unless allow_override_verified is True.
    """
    res = AdminDataService.execute_import(
        db=db,
        entity_type=payload.entity_type,
        rows=payload.rows,
        user=admin_user,
        allow_override_verified=payload.allow_override_verified,
        source_name=payload.source_name,
        source_url=payload.source_url,
        patch_version=payload.patch_version,
    )
    return res


@router.get("/export/{entity_type}")
def export_dataset(
    entity_type: str,
    format: str = Query("JSON", description="JSON or CSV"),
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Exports entities (MOVES, COMBOS, STAGES, SOURCES) in JSON or CSV with all provenance metadata.
    """
    try:
        content = AdminDataService.export_data(db=db, entity_type=entity_type, format_type=format)
        media_type = "application/json" if format.upper() == "JSON" else "text/csv"
        filename = f"{entity_type.lower()}_export.{format.lower()}"
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/audit/integrity", response_model=DatabaseAuditReport)
def run_database_integrity_audit(
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Executes a comprehensive non-destructive audit of the entire database.
    Checks relational invariants, broken foreign keys, physical fighting game bounds,
    hazard compatibility, and missing-value semantics.
    """
    return DataValidator.audit_entire_database(db)


@router.post("/validate/move", response_model=ValidationResult)
def validate_move_data(
    payload: MoveValidationRequest,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Validates a single move record against physical Tekken frame bounds,
    missing-value semantics, notation syntax, and character existence.
    """
    return DataValidator.validate_move(payload.model_dump(), db=db)


@router.post("/validate/combo", response_model=ValidationResult)
def validate_combo_data(
    payload: ComboValidationRequest,
    db: Session = Depends(get_db),
    admin_user: str = Depends(verify_admin_token),
):
    """
    Validates a single combo record against starter move ownership,
    stage hazard compatibility, damage/hit bounds, and difficulty.
    """
    return DataValidator.validate_combo(payload.model_dump(), db=db)

