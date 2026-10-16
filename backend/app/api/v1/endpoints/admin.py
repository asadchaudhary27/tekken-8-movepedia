from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
import os
from fastapi import APIRouter, Depends, HTTPException, Query, Response, Request, status
from fastapi.responses import PlainTextResponse, FileResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.core.admin_auth import verify_admin_token, get_current_admin_user
from backend.app.models.source import DataSource
from backend.app.models.patch import GamePatch
from backend.app.models.verification import VerificationRecord
from backend.app.models.move import Move
from backend.app.models.character import Character
from backend.app.models.admin_user import AdminUser
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    check_rate_limit,
    record_failed_attempt,
    reset_rate_limit,
    generate_totp_secret,
    get_totp_provisioning_uri,
    generate_qr_code_base64,
    verify_totp_code,
)
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
from backend.app.schemas.admin_auth import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminUserRead,
    AdminUserCreate,
    ChangePasswordRequest,
    ResetPasswordRequest,
    TOTPSetupResponse,
    TOTPVerifyRequest,
    TOTPDisableRequest,
    FighterBioUpdateRequest,
)
from backend.app.services.data_validator import DataValidator
from backend.app.services.admin_data_service import AdminDataService

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


# ===========================================================================
# ENTERPRISE ADMIN AUTHENTICATION & MANAGEMENT ENDPOINTS
# ===========================================================================

@router.post("/login", response_model=AdminLoginResponse)
def admin_login(
    payload: AdminLoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Authenticates an administrator using Username OR Email + Password.
    Includes brute-force lockout (5 failed attempts = 15m lockout) and optional TOTP 2FA.
    """
    ident = payload.username_or_email.strip().lower()
    client_ip = request.client.host if request.client else "unknown"

    # 1. Rate Limiting Check (by identifier and client IP)
    blocked, wait_secs = check_rate_limit(ident)
    if not blocked:
        blocked, wait_secs = check_rate_limit(client_ip)
    if blocked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account temporarily locked due to excessive failed attempts. Please retry in {wait_secs} seconds."
        )

    # 2. Lookup AdminUser
    user = db.query(AdminUser).filter(
        (AdminUser.username.ilike(ident)) | (AdminUser.email.ilike(ident))
    ).first()

    now = datetime.now(timezone.utc)
    if not user:
        record_failed_attempt(ident)
        record_failed_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    # Check database-level account lock
    if user.locked_until and user.locked_until.replace(tzinfo=timezone.utc) > now:
        remaining = int((user.locked_until.replace(tzinfo=timezone.utc) - now).total_seconds())
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account is locked. Please try again in {remaining} seconds."
        )

    # 3. Verify Password
    if not verify_password(payload.password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = now + timedelta(minutes=15)
        db.commit()
        record_failed_attempt(ident)
        record_failed_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    # 4. Check TOTP 2FA if enabled
    if user.totp_enabled:
        if not payload.totp_code:
            return AdminLoginResponse(
                access_token=None,
                requires_2fa=True,
                message="Two-factor authentication code required."
            )
        if not verify_totp_code(user.totp_secret, payload.totp_code):
            record_failed_attempt(ident)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 6-digit Authenticator code. Please check your app and try again."
            )

    # 5. Success: Reset lockouts & issue signed JWT
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = now
    db.commit()

    reset_rate_limit(ident)
    reset_rate_limit(client_ip)

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role
    })

    return AdminLoginResponse(
        access_token=token,
        token_type="bearer",
        requires_2fa=False,
        user=AdminUserRead.model_validate(user),
        message=f"Welcome back, {user.username}."
    )


@router.get("/me", response_model=AdminUserRead)
def get_current_admin_profile(
    current_user: AdminUser = Depends(get_current_admin_user)
):
    """Returns profile information for the authenticated admin user."""
    return current_user


@router.post("/change-password")
def change_admin_password(
    payload: ChangePasswordRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Allows authenticated admin to change their own password."""
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password does not match.")
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirmation do not match.")
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")

    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"status": "SUCCESS", "message": "Password changed successfully."}


@router.get("/users", response_model=List[AdminUserRead])
def list_admin_users(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Lists all registered administrative accounts."""
    return db.query(AdminUser).order_by(AdminUser.id).all()


@router.post("/users", response_model=AdminUserRead)
def create_admin_user(
    payload: AdminUserCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """SuperAdmin self-service tool to create a new admin or editor account."""
    if current_user.role != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Only SuperAdmins can create new admin accounts.")

    existing = db.query(AdminUser).filter(
        (AdminUser.username == payload.username) | (AdminUser.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email is already registered.")

    new_user = AdminUser(
        username=payload.username.strip(),
        email=payload.email.strip().lower(),
        password_hash=hash_password(payload.password),
        role=payload.role,
        totp_enabled=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/users/{user_id}")
def delete_admin_user(
    user_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Deletes or revokes a secondary admin user."""
    if current_user.role != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Only SuperAdmins can delete accounts.")
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete your own active superadmin account.")

    target = db.query(AdminUser).filter_by(id=user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Admin user not found.")

    db.delete(target)
    db.commit()
    return {"status": "SUCCESS", "message": f"Admin user '{target.username}' revoked successfully."}


@router.post("/users/{user_id}/reset-password")
def reset_secondary_admin_password(
    user_id: int,
    payload: ResetPasswordRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """SuperAdmin resets password for another admin user."""
    if current_user.role != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Only SuperAdmins can reset passwords.")

    target = db.query(AdminUser).filter_by(id=user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Admin user not found.")

    target.password_hash = hash_password(payload.new_password)
    target.failed_login_attempts = 0
    target.locked_until = None
    db.commit()
    return {"status": "SUCCESS", "message": f"Password reset for '{target.username}'."}


# ---------------------------------------------------------------------------
# 2FA TOTP Authenticator Activation & Management
# ---------------------------------------------------------------------------

@router.post("/2fa/setup", response_model=TOTPSetupResponse)
def setup_totp_authenticator(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Generates a new TOTP secret and QR code for Google Authenticator / Authy.
    Does not activate 2FA until user verifies with an actual code.
    """
    secret = generate_totp_secret()
    current_user.totp_secret = secret
    db.commit()

    uri = get_totp_provisioning_uri(current_user.username, secret)
    qr_base64 = generate_qr_code_base64(uri)

    return TOTPSetupResponse(
        secret=secret,
        provisioning_uri=uri,
        qr_code_base64=qr_base64,
        manual_entry_key=secret
    )


@router.post("/2fa/enable")
def enable_totp_authenticator(
    payload: TOTPVerifyRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Verifies a test 6-digit code and activates 2FA for the account."""
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="Run /2fa/setup first to generate a secret.")

    if not verify_totp_code(current_user.totp_secret, payload.code):
        raise HTTPException(status_code=400, detail="Invalid 6-digit code. Check your Authenticator app.")

    current_user.totp_enabled = True
    db.commit()
    return {"status": "SUCCESS", "message": "Two-Factor Authentication is now ENABLED."}


@router.post("/2fa/disable")
def disable_totp_authenticator(
    payload: TOTPDisableRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Disables 2FA after password confirmation (switches back to standard login)."""
    if not verify_password(payload.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Password incorrect. Cannot disable 2FA.")

    current_user.totp_enabled = False
    current_user.totp_secret = None
    db.commit()
    return {"status": "SUCCESS", "message": "Two-Factor Authentication is now DISABLED (Standard Login active)."}


# ---------------------------------------------------------------------------
# Database Backup & Maintenance
# ---------------------------------------------------------------------------

@router.get("/database/backup")
def download_database_backup(
    current_user: AdminUser = Depends(get_current_admin_user),
):
    """Securely downloads a copy of the SQLite database."""
    db_file = os.path.abspath("tekken8_fyp.db")
    if not os.path.exists(db_file):
        raise HTTPException(status_code=404, detail="Database file not found.")

    return FileResponse(
        path=db_file,
        filename=f"tekken8_esports_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
        media_type="application/x-sqlite3"
    )


@router.put("/fighters/{slug}/bio")
def update_fighter_bio(
    slug: str,
    payload: FighterBioUpdateRequest,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Updates fighter biographical and lore metadata."""
    char = db.query(Character).filter_by(slug=slug).first()
    if not char:
        raise HTTPException(status_code=404, detail=f"Fighter '{slug}' not found.")

    if payload.avatar_url:
        char.avatar_url = payload.avatar_url
    if payload.bio_summary:
        char.hurtbox_notes = payload.bio_summary
    if payload.origin:
        char.archetype = payload.origin
    db.commit()
    return {"status": "SUCCESS", "message": f"Bio updated for {char.name}", "slug": slug}



