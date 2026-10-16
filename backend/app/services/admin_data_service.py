import csv
import io
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func

from backend.app.core.config import settings
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.combo_compatibility import ComboCompatibility
from backend.app.models.matchup_note import MatchupNote
from backend.app.models.practice import PracticeRecord
from backend.app.models.source import DataSource
from backend.app.models.patch import GamePatch
from backend.app.models.verification import VerificationRecord
from backend.app.models.conflict import DataConflict
from backend.app.models.missing_data import MissingDataIssue
from backend.app.models.import_batch import ImportBatch
from backend.app.schemas.admin import (
    QualityDashboardStats,
    MoveAdminCreateUpdate,
    ComboAdminCreateUpdate,
    StageMechanicsAdminUpdate,
    MatchupNoteAdminUpdate,
    CompatibilityAdminUpdate,
    ImportPreviewResponse,
    ImportRowIssue,
    ImportSummaryResponse,
)
from backend.app.services.data_validator import DataValidator



class AdminDataService:
    """
    Core administrative service managing:
    - Quality dashboard analytics and audit alerts
    - Non-destructive record creation and updates with full change audit trail
    - CSV/JSON transaction-safe imports with preview, duplicate/conflict detection
    - Prevention of unverified data silently overwriting verified data
    - Entity exports with complete provenance
    """

    @classmethod
    def get_quality_dashboard(cls, db: Session) -> QualityDashboardStats:
        total_chars = db.query(Character).count()
        total_stages = db.query(Stage).count()
        total_moves = db.query(Move).count()
        total_combos = db.query(ComboRoute).count()
        total_verif = db.query(VerificationRecord).count()

        audit_issues: List[Dict[str, Any]] = []

        # 1. Missing Frame Data (Excluding legitimate non-strikes: stances, command throws, parries, unblockables)
        missing_frame_moves = (
            db.query(Move)
            .filter(
                ~func.lower(func.coalesce(Move.hit_level, '')).in_(["s", "t", "ub", "throw", "parry", "reversal", "special", "none", ""]),
                ~Move.name.ilike("%stance%"),
                ~Move.name.ilike("%form%"),
                ~Move.name.ilike("%parry%"),
                ~Move.name.ilike("%shield%"),
                ~Move.name.ilike("%swing%"),
                ~Move.name.ilike("%wizard%"),
                ~Move.name.ilike("%buster%"),
                ~Move.name.ilike("%step%"),
                ~Move.name.ilike("%entry%"),
                ~Move.name.ilike("%piledriver%"),
                ~Move.name.ilike("%hug%"),
                ~Move.name.ilike("%gouge%"),
                ~Move.name.ilike("%pirouette%"),
                ~Move.name.ilike("%dragonfly%"),
                ~Move.name.ilike("%judgment%"),
                ~Move.name.ilike("%phoenix%"),
                ~Move.name.ilike("%dance%"),
                ~Move.name.ilike("%mist%"),
                ~Move.name.ilike("%laser%"),
                or_(
                    Move.startup_frames.is_(None),
                    Move.block_advantage.is_(None),
                    Move.hit_advantage.is_(None),
                )
            )
            .all()
        )
        missing_frame_count = len(missing_frame_moves)
        for m in missing_frame_moves[:10]:
            char_name = m.character.name if m.character else "Unknown"
            audit_issues.append({
                "severity": "HIGH",
                "entity_type": "MOVE",
                "entity_id": m.id,
                "title": f"{char_name}: {m.name or m.normalized_notation}",
                "issue_type": "MISSING_FRAME_DATA",
                "status": "NOT_PROVIDED" if not m.startup_raw else "UNKNOWN",
                "details": f"Missing strike frame metrics (Startup: {m.startup_frames or 'None'}, Block: {m.block_advantage or 'None'})",
            })

        # 2. Missing Stage Mechanics (Only true missing geometry or location)
        incomplete_stages = (
            db.query(Stage)
            .filter(
                or_(
                    Stage.boundary_shape.is_(None),
                    Stage.location.is_(None),
                )
            )
            .all()
        )
        missing_stage_count = len(incomplete_stages)
        for s in incomplete_stages:
            audit_issues.append({
                "severity": "MEDIUM",
                "entity_type": "STAGE",
                "entity_id": s.id,
                "title": f"Stage: {s.name}",
                "issue_type": "MISSING_STAGE_MECHANICS",
                "status": "NOT_PROVIDED",
                "details": f"Hazard interactions or layout geometry incomplete (Wall Break: {s.wall_break})",
            })

        # 3. Combos without Opponent Compatibility (Excluding Universal combos)
        combos_without_compat: List[ComboRoute] = (
            db.query(ComboRoute)
            .filter(
                ComboRoute.target_hurtbox_class != "UNIVERSAL",
                ~ComboRoute.compatibilities.any()
            )
            .all()
        )
        missing_compat_count = len(combos_without_compat)
        for c in combos_without_compat[:8]:
            char_name = c.character.name if c.character else "Unknown"
            audit_issues.append({
                "severity": "LOW",
                "entity_type": "COMBO",
                "entity_id": c.id,
                "title": f"{char_name}: {c.title}",
                "issue_type": "UNTESTED_COMPATIBILITY",
                "status": "UNKNOWN_COMPATIBILITY",
                "details": "Character-specific combo route requires hurtbox testing.",
            })

        # 4. Unverified Punish Options
        unverified_punishes = (
            db.query(Move)
            .filter(Move.block_advantage <= -10, Move.verification_status == "UNVERIFIED")
            .all()
        )
        unverified_punish_count = len(unverified_punishes)
        for m in unverified_punishes[:8]:
            char_name = m.character.name if m.character else "Unknown"
            audit_issues.append({
                "severity": "HIGH",
                "entity_type": "MOVE",
                "entity_id": m.id,
                "title": f"{char_name}: {m.name or m.normalized_notation}",
                "issue_type": "UNVERIFIED_PUNISH",
                "status": "UNVERIFIED",
                "details": f"Move is punishable on block ({m.block_advantage}) but punish status is UNVERIFIED.",
            })

        # 5. Conflicting Records
        conflicts = db.query(DataConflict).filter(DataConflict.resolution_status == "UNRESOLVED").all()
        conflicting_moves = db.query(Move).filter(Move.verification_status == "CONFLICTING").all()
        conflict_count = len(conflicts) + len(conflicting_moves)
        for c in conflicts[:5]:
            audit_issues.append({
                "severity": "CRITICAL",
                "entity_type": "CONFLICT",
                "entity_id": c.id,
                "title": f"Move ID {c.move_id} Discrepancy",
                "issue_type": "CONFLICTING_DATA",
                "status": "CONFLICTING",
                "details": f"Field '{c.field_name}': Source A='{c.source_a_value}' vs Source B='{c.source_b_value}'",
            })

        # 6. Outdated Patch Records
        current_patch = settings.CURRENT_GAME_PATCH
        outdated_moves = db.query(Move).filter(Move.patch_id != None).all()
        outdated_combos = (
            db.query(ComboRoute)
            .filter(ComboRoute.patch_version != current_patch)
            .all()
        )
        outdated_patch_count = len(outdated_combos)
        for c in outdated_combos[:5]:
            audit_issues.append({
                "severity": "MEDIUM",
                "entity_type": "COMBO",
                "entity_id": c.id,
                "title": f"Combo: {c.title}",
                "issue_type": "OUTDATED_PATCH",
                "status": "OUTDATED_PATCH",
                "details": f"Recorded on patch {c.patch_version}; current active game patch is {current_patch}.",
            })

        # 7. Incomplete Source Metadata
        sources = db.query(DataSource).all()
        incomplete_sources = [s for s in sources if not s.attribution_text or not s.license_type]
        incomplete_source_count = len(incomplete_sources)
        for s in incomplete_sources:
            audit_issues.append({
                "severity": "LOW",
                "entity_type": "SOURCE",
                "entity_id": s.id,
                "title": f"Source: {s.name}",
                "issue_type": "INCOMPLETE_ATTRIBUTION",
                "status": "NOT_PROVIDED",
                "details": f"Attribution text or license link is missing for external provider.",
            })

        # 8. Records Awaiting Review
        awaiting_moves = db.query(Move).filter(Move.verification_status.in_(["UNVERIFIED", "PENDING_REVIEW"])).count()
        awaiting_combos = db.query(ComboRoute).filter(ComboRoute.verification_status.in_(["UNVERIFIED", "PENDING_REVIEW"])).count()
        awaiting_review_count = awaiting_moves + awaiting_combos

        # Status Distribution
        verified_count = (
            db.query(Move).filter(Move.verification_status == "VERIFIED").count()
            + db.query(ComboRoute).filter(ComboRoute.verification_status == "VERIFIED").count()
        )
        unverified_count = (
            db.query(Move).filter(Move.verification_status == "UNVERIFIED").count()
            + db.query(ComboRoute).filter(ComboRoute.verification_status == "UNVERIFIED").count()
        )
        conflicting_count = (
            db.query(Move).filter(Move.verification_status == "CONFLICTING").count()
            + db.query(ComboRoute).filter(ComboRoute.verification_status == "CONFLICTING").count()
        )
        unavailable_count = (
            db.query(Move).filter(Move.verification_status == "UNAVAILABLE").count()
            + db.query(ComboRoute).filter(ComboRoute.verification_status == "UNAVAILABLE").count()
        )
        confirmed_absent = db.query(Move).filter(Move.verification_status == "CONFIRMED_ABSENT").count()

        status_dist = {
            "VERIFIED": verified_count,
            "UNVERIFIED": unverified_count,
            "CONFLICTING": conflicting_count,
            "UNAVAILABLE": unavailable_count,
            "CONFIRMED_ABSENT": confirmed_absent,
            "UNKNOWN": missing_frame_count + missing_compat_count,
            "NOT_PROVIDED": missing_stage_count + incomplete_source_count,
            "NOT_APPLICABLE": 0,
        }

        return QualityDashboardStats(
            total_characters=total_chars,
            total_stages=total_stages,
            total_moves=total_moves,
            total_combos=total_combos,
            total_verification_records=total_verif,
            missing_frame_data_count=missing_frame_count,
            missing_stage_mechanics_count=missing_stage_count,
            combos_without_opponent_compatibility_count=missing_compat_count,
            unverified_punish_options_count=unverified_punish_count,
            conflicting_records_count=conflict_count,
            outdated_patch_records_count=outdated_patch_count,
            incomplete_source_metadata_count=incomplete_source_count,
            records_awaiting_review_count=awaiting_review_count,
            status_distribution=status_dist,
            audit_issues=audit_issues,
        )

    # --------------------------------------------------------------------------
    # Non-Destructive Audit Trail Logging
    # --------------------------------------------------------------------------
    @classmethod
    def log_audit_trail(
        cls,
        db: Session,
        entity_type: str,
        entity_id: Optional[int],
        field_name: Optional[str],
        old_val: Any,
        new_val: Any,
        user: str,
        method: str,
        result: str,
        notes: str,
        patch_version: str = "3.00.02",
        source_url: Optional[str] = None,
        move_id: Optional[int] = None,
    ) -> VerificationRecord:
        """
        Preserves complete history without deleting prior records.
        """
        rec = VerificationRecord(
            entity_type=entity_type.upper(),
            entity_id=entity_id,
            move_id=move_id if move_id else (entity_id if entity_type.upper() == "MOVE" else None),
            field_name=field_name,
            old_value=str(old_val) if old_val is not None else None,
            new_value=str(new_val) if new_val is not None else None,
            verified_by=user,
            method=method,
            result=result,
            evidence_notes=notes,
            change_summary=f"Changed {field_name or entity_type} from '{old_val}' to '{new_val}'",
            patch_version=patch_version,
            source_url=source_url,
            verified_at=datetime.now(timezone.utc),
        )
        db.add(rec)
        return rec

    # --------------------------------------------------------------------------
    # Record Creation & Modification Operations
    # --------------------------------------------------------------------------
    @classmethod
    def update_verification_status(
        cls,
        db: Session,
        entity_type: str,
        entity_id: int,
        new_status: str,
        evidence: str,
        user: str,
        source_url: Optional[str] = None,
        patch_version: str = "3.00.02",
    ) -> Dict[str, Any]:
        valid_statuses = {"VERIFIED", "UNVERIFIED", "CONFLICTING", "UNAVAILABLE", "CONFIRMED_ABSENT"}
        if new_status.upper() not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        old_status = "UNKNOWN"
        e_type = entity_type.upper()

        if e_type == "MOVE":
            move = db.query(Move).filter_by(id=entity_id).first()
            if not move:
                raise ValueError(f"Move with id {entity_id} not found.")
            old_status = move.verification_status
            move.verification_status = new_status.upper()
            move.verification_notes = evidence
        elif e_type == "COMBO":
            combo = db.query(ComboRoute).filter_by(id=entity_id).first()
            if not combo:
                raise ValueError(f"Combo with id {entity_id} not found.")
            old_status = combo.verification_status
            combo.verification_status = new_status.upper()
        elif e_type == "MATCHUP_NOTE":
            note = db.query(MatchupNote).filter_by(id=entity_id).first()
            if not note:
                raise ValueError(f"MatchupNote with id {entity_id} not found.")
            old_status = note.verification_status
            note.verification_status = new_status.upper()
        elif e_type == "COMPATIBILITY":
            comp = db.query(ComboCompatibility).filter_by(id=entity_id).first()
            if not comp:
                raise ValueError(f"ComboCompatibility with id {entity_id} not found.")
            old_status = comp.compatibility_status
            comp.compatibility_status = new_status.upper()
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        # Non-destructive audit record
        cls.log_audit_trail(
            db=db,
            entity_type=e_type,
            entity_id=entity_id,
            field_name="verification_status",
            old_val=old_status,
            new_val=new_status.upper(),
            user=user,
            method="MANUAL_AUDIT_STATUS_UPDATE",
            result=new_status.upper(),
            notes=evidence,
            patch_version=patch_version,
            source_url=source_url,
        )
        db.commit()

        return {
            "entity_type": e_type,
            "entity_id": entity_id,
            "old_status": old_status,
            "new_status": new_status.upper(),
            "updated_by": user,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @classmethod
    def save_move(cls, db: Session, data: MoveAdminCreateUpdate, user: str) -> Move:
        char = db.query(Character).filter_by(id=data.character_id).first()
        if not char:
            raise ValueError(f"Character id {data.character_id} not found.")

        move = (
            db.query(Move)
            .filter_by(character_id=data.character_id, normalized_notation=data.normalized_notation)
            .first()
        )

        if move:
            # Record change history for each changed field
            fields_to_check = [
                ("name", move.name, data.name),
                ("startup_frames", move.startup_frames, data.startup_frames),
                ("block_advantage", move.block_advantage, data.block_advantage),
                ("hit_advantage", move.hit_advantage, data.hit_advantage),
                ("damage", move.damage, data.damage),
                ("hit_level", move.hit_level, data.hit_level),
                ("verification_status", move.verification_status, data.verification_status),
            ]
            for f_name, old_v, new_v in fields_to_check:
                if old_v != new_v and new_v is not None:
                    cls.log_audit_trail(
                        db=db,
                        entity_type="MOVE",
                        entity_id=move.id,
                        field_name=f_name,
                        old_val=old_v,
                        new_val=new_v,
                        user=user,
                        method="ADMIN_MANUAL_EDIT",
                        result=data.verification_status,
                        notes=data.reason_for_change,
                        patch_version=data.patch_version,
                        source_url=data.source_url,
                        move_id=move.id,
                    )

            move.name = data.name
            move.original_notation = data.original_notation or data.normalized_notation
            move.startup_frames = data.startup_frames
            move.block_advantage = data.block_advantage
            move.hit_advantage = data.hit_advantage
            move.ch_advantage = data.ch_advantage
            move.damage = data.damage
            move.hit_level = data.hit_level
            move.stance_context = data.stance_context
            move.verification_status = data.verification_status
            move.verification_notes = data.verification_notes
        else:
            move = Move(
                character_id=data.character_id,
                name=data.name,
                original_notation=data.original_notation or data.normalized_notation,
                normalized_notation=data.normalized_notation,
                startup_frames=data.startup_frames,
                block_advantage=data.block_advantage,
                hit_advantage=data.hit_advantage,
                ch_advantage=data.ch_advantage,
                damage=data.damage,
                hit_level=data.hit_level,
                stance_context=data.stance_context,
                verification_status=data.verification_status,
                verification_notes=data.verification_notes,
            )
            db.add(move)
            db.flush()

            cls.log_audit_trail(
                db=db,
                entity_type="MOVE",
                entity_id=move.id,
                field_name="CREATE_RECORD",
                old_val=None,
                new_val=f"{char.name} {data.name} ({data.normalized_notation})",
                user=user,
                method="ADMIN_MANUAL_CREATE",
                result=data.verification_status,
                notes=data.reason_for_change,
                patch_version=data.patch_version,
                source_url=data.source_url,
                move_id=move.id,
            )

        db.commit()
        db.refresh(move)
        return move

    @classmethod
    def save_combo(cls, db: Session, data: ComboAdminCreateUpdate, user: str) -> ComboRoute:
        char = db.query(Character).filter_by(id=data.character_id).first()
        if not char:
            raise ValueError(f"Character id {data.character_id} not found.")

        combo = None
        if data.id:
            combo = db.query(ComboRoute).filter_by(id=data.id).first()

        if combo:
            cls.log_audit_trail(
                db=db,
                entity_type="COMBO",
                entity_id=combo.id,
                field_name="total_damage",
                old_val=combo.total_damage,
                new_val=data.total_damage,
                user=user,
                method="ADMIN_COMBO_EDIT",
                result=data.verification_status,
                notes=data.reason_for_change,
                patch_version=data.patch_version,
            )
            combo.title = data.title
            combo.notation_sequence = data.notation_sequence
            combo.total_damage = data.total_damage
            combo.hit_count = data.hit_count
            combo.difficulty = data.difficulty
            combo.combo_type = data.combo_type
            combo.launcher_type = data.launcher_type
            combo.uses_heat = data.uses_heat
            combo.uses_tornado = data.uses_tornado
            combo.uses_wall = data.uses_wall
            combo.requires_counter_hit = data.requires_counter_hit
            combo.is_stage_dependent = data.is_stage_dependent
            combo.stage_id = data.stage_id
            combo.stage_section = data.stage_section
            combo.starter_move_name = data.starter_move_name
            combo.starter_move_input = data.starter_move_input
            combo.ender_move_name = data.ender_move_name
            combo.ender_move_input = data.ender_move_input
            combo.damage_type = data.damage_type
            combo.damage_calculation_method = data.damage_calculation_method
            combo.raw_damage_sum = data.raw_damage_sum
            combo.required_stance = data.required_stance
            combo.execution_notes = data.execution_notes
            combo.target_hurtbox_class = data.target_hurtbox_class
            combo.easier_alternative_id = data.easier_alternative_id
            combo.easier_alternative_notes = data.easier_alternative_notes
            combo.verification_status = data.verification_status
            combo.patch_version = data.patch_version
            combo.source = data.source
        else:
            combo = ComboRoute(
                character_id=data.character_id,
                title=data.title,
                notation_sequence=data.notation_sequence,
                total_damage=data.total_damage,
                hit_count=data.hit_count,
                difficulty=data.difficulty,
                combo_type=data.combo_type,
                launcher_type=data.launcher_type,
                uses_heat=data.uses_heat,
                uses_tornado=data.uses_tornado,
                uses_wall=data.uses_wall,
                requires_counter_hit=data.requires_counter_hit,
                is_stage_dependent=data.is_stage_dependent,
                stage_id=data.stage_id,
                stage_section=data.stage_section,
                starter_move_name=data.starter_move_name,
                starter_move_input=data.starter_move_input,
                ender_move_name=data.ender_move_name,
                ender_move_input=data.ender_move_input,
                damage_type=data.damage_type,
                damage_calculation_method=data.damage_calculation_method,
                raw_damage_sum=data.raw_damage_sum,
                required_stance=data.required_stance,
                execution_notes=data.execution_notes,
                target_hurtbox_class=data.target_hurtbox_class,
                easier_alternative_id=data.easier_alternative_id,
                easier_alternative_notes=data.easier_alternative_notes,
                verification_status=data.verification_status,
                patch_version=data.patch_version,
                source=data.source,
            )
            db.add(combo)
            db.flush()

            cls.log_audit_trail(
                db=db,
                entity_type="COMBO",
                entity_id=combo.id,
                field_name="CREATE_RECORD",
                old_val=None,
                new_val=f"{char.name} combo: {data.title}",
                user=user,
                method="ADMIN_COMBO_CREATE",
                result=data.verification_status,
                notes=data.reason_for_change,
                patch_version=data.patch_version,
            )

        db.commit()
        db.refresh(combo)
        return combo

    @classmethod
    def save_stage_mechanics(cls, db: Session, stage_id: int, data: StageMechanicsAdminUpdate, user: str) -> Stage:
        st = db.query(Stage).filter_by(id=stage_id).first()
        if not st:
            raise ValueError(f"Stage with id {stage_id} not found.")

        cls.log_audit_trail(
            db=db,
            entity_type="STAGE",
            entity_id=st.id,
            field_name="stage_mechanics",
            old_val=f"Walls:{st.has_walls},WB:{st.wall_break},FB:{st.floor_break}",
            new_val=f"Walls:{data.has_walls},WB:{data.wall_break},FB:{data.floor_break}",
            user=user,
            method="ADMIN_STAGE_UPDATE",
            result="VERIFIED",
            notes=data.reason_for_change,
        )

        st.has_walls = data.has_walls
        st.boundary_shape = data.boundary_shape
        st.wall_distance = data.wall_distance
        st.wall_break = data.wall_break
        st.hard_wall_break = data.hard_wall_break
        st.wall_blast = data.wall_blast
        st.floor_break = data.floor_break
        st.floor_blast = data.floor_blast
        st.balcony_break = data.balcony_break
        st.special_mechanics = data.special_mechanics
        st.notes = data.notes

        db.commit()
        db.refresh(st)
        return st

    # --------------------------------------------------------------------------
    # Transaction-Safe Import System with Strict Verified Data Protection
    # --------------------------------------------------------------------------
    @classmethod
    def parse_raw_import_content(cls, raw_content: str, format_type: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        fmt = format_type.upper().strip()

        if fmt == "JSON":
            try:
                parsed = json.loads(raw_content)
                if isinstance(parsed, list):
                    rows = parsed
                elif isinstance(parsed, dict):
                    rows = [parsed]
                else:
                    raise ValueError("JSON must be a list of records or a record dictionary.")
            except Exception as e:
                raise ValueError(f"Failed to parse JSON payload: {str(e)}")
        elif fmt == "CSV":
            try:
                reader = csv.DictReader(io.StringIO(raw_content.strip()))
                rows = [row for row in reader]
            except Exception as e:
                raise ValueError(f"Failed to parse CSV payload: {str(e)}")
        else:
            raise ValueError(f"Unsupported format: {format_type}. Use JSON or CSV.")

        return rows

    @classmethod
    def preview_import(
        cls,
        db: Session,
        entity_type: str,
        raw_content: str,
        format_type: str = "JSON",
        source_name: str = "Manual Import",
        patch_version: str = "3.00.02",
        field_mapping: Optional[Dict[str, str]] = None,
    ) -> ImportPreviewResponse:
        rows = cls.parse_raw_import_content(raw_content, format_type)
        e_type = entity_type.upper()

        issues: List[ImportRowIssue] = []
        preview_rows: List[Dict[str, Any]] = []

        valid_count = 0
        error_count = 0
        duplicate_count = 0
        conflict_count = 0
        protected_count = 0

        # Pre-cache characters for fast lookup
        chars_by_slug = {c.slug: c for c in db.query(Character).all()}
        chars_by_id = {c.id: c for c in chars_by_slug.values()}

        for idx, row in enumerate(rows):
            # Apply field mapping if provided
            mapped_row = dict(row)
            if field_mapping:
                for src_field, tgt_field in field_mapping.items():
                    if src_field in mapped_row:
                        mapped_row[tgt_field] = mapped_row.pop(src_field)

            row_has_error = False

            if e_type == "MOVES":
                # Validation: character_id or character_slug
                char = None
                char_id = mapped_row.get("character_id")
                char_slug = mapped_row.get("character_slug")
                if char_id and int(char_id) in chars_by_id:
                    char = chars_by_id[int(char_id)]
                elif char_slug and char_slug in chars_by_slug:
                    char = chars_by_slug[char_slug]

                if not char:
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR",
                            field="character_id",
                            message="Invalid or missing character reference.",
                            incoming_data=mapped_row,
                        )
                    )
                    error_count += 1
                    row_has_error = True

                notation = mapped_row.get("normalized_notation") or mapped_row.get("notation")
                if not notation:
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR",
                            field="normalized_notation",
                            message="Move notation is required.",
                            incoming_data=mapped_row,
                        )
                    )
                    error_count += 1
                    row_has_error = True

                if char and notation:
                    # Check for existing move
                    existing_move = (
                        db.query(Move)
                        .filter_by(character_id=char.id, normalized_notation=notation)
                        .first()
                    )
                    if existing_move:
                        duplicate_count += 1
                        incoming_status = mapped_row.get("verification_status", "UNVERIFIED").upper()

                        # STRICT RULE: Never silently overwrite verified data with unverified import
                        if existing_move.verification_status == "VERIFIED" and incoming_status != "VERIFIED":
                            protected_count += 1
                            issues.append(
                                ImportRowIssue(
                                    row_index=idx + 1,
                                    issue_type="UNVERIFIED_OVERWRITE_PROTECTED",
                                    field="verification_status",
                                    message=(
                                        f"PROTECTION: Existing move '{char.name} {notation}' is VERIFIED in DB. "
                                        f"Incoming unverified import ({incoming_status}) will NOT overwrite verified data without explicit admin override flag."
                                    ),
                                    incoming_data=mapped_row,
                                )
                            )

                        # Detect frame discrepancies
                        in_startup = mapped_row.get("startup_frames")
                        if in_startup is not None and existing_move.startup_frames is not None:
                            try:
                                if int(in_startup) != existing_move.startup_frames:
                                    conflict_count += 1
                                    issues.append(
                                        ImportRowIssue(
                                            row_index=idx + 1,
                                            issue_type="CONFLICT",
                                            field="startup_frames",
                                            message=f"Discrepancy: existing startup is i{existing_move.startup_frames}, incoming is i{in_startup}.",
                                            incoming_data=mapped_row,
                                        )
                                    )
                            except ValueError:
                                pass

                # Advanced semantic validation via DataValidator
                move_val = DataValidator.validate_move(mapped_row, db=db)
                for v_issue in move_val.issues:
                    if v_issue.rule in ["DUPLICATE_MOVE_NOTATION", "BROKEN_CHARACTER_REFERENCE", "REQUIRED_NOTATION"]:
                        continue
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR" if v_issue.severity in ["CRITICAL", "ERROR"] else "WARNING",
                            field=v_issue.field,
                            message=v_issue.message,
                            incoming_data=mapped_row,
                        )
                    )
                    if v_issue.severity in ["CRITICAL", "ERROR"]:
                        error_count += 1
                        row_has_error = True

            elif e_type == "COMBOS":
                title = mapped_row.get("title")
                notation = mapped_row.get("notation_sequence")
                if not title or not notation:
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR",
                            field="title",
                            message="Combo title and notation_sequence are required.",
                            incoming_data=mapped_row,
                        )
                    )
                    error_count += 1
                    row_has_error = True

                char_id = mapped_row.get("character_id")
                if not char_id or int(char_id) not in chars_by_id:
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR",
                            field="character_id",
                            message="Valid character_id is required.",
                            incoming_data=mapped_row,
                        )
                    )
                    error_count += 1
                    row_has_error = True

                # Duplicate combo check
                if title and char_id:
                    exist_combo = (
                        db.query(ComboRoute)
                        .filter_by(character_id=int(char_id), title=title)
                        .first()
                    )
                    if exist_combo:
                        duplicate_count += 1
                        if exist_combo.verification_status == "VERIFIED" and mapped_row.get("verification_status") != "VERIFIED":
                            protected_count += 1
                            issues.append(
                                ImportRowIssue(
                                    row_index=idx + 1,
                                    issue_type="UNVERIFIED_OVERWRITE_PROTECTED",
                                    field="verification_status",
                                    message=f"PROTECTION: Existing combo '{title}' is VERIFIED. Incoming unverified data will not overwrite verified record.",
                                    incoming_data=mapped_row,
                                )
                            )

                # Advanced semantic validation via DataValidator
                combo_val = DataValidator.validate_combo(mapped_row, db=db)
                for v_issue in combo_val.issues:
                    if v_issue.rule in ["REQUIRED_TITLE", "REQUIRED_COMBO_SEQUENCE", "BROKEN_CHARACTER_REFERENCE"]:
                        continue
                    issues.append(
                        ImportRowIssue(
                            row_index=idx + 1,
                            issue_type="ERROR" if v_issue.severity in ["CRITICAL", "ERROR"] else "WARNING",
                            field=v_issue.field,
                            message=v_issue.message,
                            incoming_data=mapped_row,
                        )
                    )
                    if v_issue.severity in ["CRITICAL", "ERROR"]:
                        error_count += 1
                        row_has_error = True


            if not row_has_error:
                valid_count += 1

            if len(preview_rows) < 20:
                preview_rows.append(mapped_row)

        return ImportPreviewResponse(
            entity_type=e_type,
            total_rows=len(rows),
            valid_rows_count=valid_count,
            error_rows_count=error_count,
            duplicate_count=duplicate_count,
            conflict_count=conflict_count,
            verified_protection_count=protected_count,
            is_importable=(error_count == 0),
            preview_rows=preview_rows,
            issues=issues,
        )

    @classmethod
    def execute_import(
        cls,
        db: Session,
        entity_type: str,
        rows: List[Dict[str, Any]],
        user: str,
        allow_override_verified: bool = False,
        source_name: str = "Manual Import",
        source_url: Optional[str] = None,
        patch_version: str = "3.00.02",
    ) -> ImportSummaryResponse:
        """
        Executes a transaction-safe import with rollback on failure.
        Ensures unverified incoming data NEVER silently overwrites verified records.
        """
        e_type = entity_type.upper()
        created_count = 0
        updated_count = 0
        skipped_count = 0
        conflicts_count = 0
        audit_count = 0

        # Ensure DataSource exists
        data_src = db.query(DataSource).filter_by(name=source_name).first()
        if not data_src:
            data_src = DataSource(
                name=source_name,
                base_url=source_url or "https://tekkendocs.com",
                license_type="Community Fair Use / Research",
                approval_status="APPROVED_FOR_USE",
            )
            db.add(data_src)
            db.flush()

        import_batch = ImportBatch(
            source_id=data_src.id,
            source_url=source_url or "https://tekkendocs.com",
            patch_version=patch_version,
            status="IN_PROGRESS",
            total_records=len(rows),
        )
        db.add(import_batch)
        db.flush()

        try:
            for idx, row in enumerate(rows):
                if e_type == "MOVES":
                    char_id = row.get("character_id")
                    if not char_id:
                        char_slug = row.get("character_slug")
                        char = db.query(Character).filter_by(slug=char_slug).first()
                        if char:
                            char_id = char.id
                    if not char_id:
                        raise ValueError(f"Row {idx+1}: Missing character_id.")

                    notation = row.get("normalized_notation") or row.get("notation")
                    if not notation:
                        raise ValueError(f"Row {idx+1}: Missing notation.")

                    # Strict validation check via DataValidator
                    move_val = DataValidator.validate_move(row, db=db)
                    critical_errors = [i for i in move_val.issues if i.severity in ["CRITICAL", "ERROR"] and i.rule != "DUPLICATE_MOVE_NOTATION"]
                    if critical_errors:
                        raise ValueError(f"Row {idx+1} ({notation}): {critical_errors[0].message}")


                    move = (
                        db.query(Move)
                        .filter_by(character_id=int(char_id), normalized_notation=notation)
                        .first()
                    )
                    incoming_status = row.get("verification_status", "UNVERIFIED").upper()

                    if move:
                        # PROTECTION: Never silently overwrite verified data with unverified import
                        if move.verification_status == "VERIFIED" and incoming_status != "VERIFIED":
                            if not allow_override_verified:
                                # Log conflict and skip
                                conflict = DataConflict(
                                    move_id=move.id,
                                    field_name="verification_status",
                                    source_a_value=f"VERIFIED ({move.block_advantage})",
                                    source_b_value=f"UNVERIFIED_IMPORT ({row.get('block_advantage')})",
                                    resolution_status="UNRESOLVED",
                                    resolution_notes=f"Attempted unverified import from '{source_name}' rejected under verified preservation policy.",
                                )
                                db.add(conflict)
                                conflicts_count += 1
                                skipped_count += 1
                                continue
                            else:
                                # Overwrite was explicitly authorized: record in audit history!
                                cls.log_audit_trail(
                                    db=db,
                                    entity_type="MOVE",
                                    entity_id=move.id,
                                    field_name="OVERRIDE_VERIFIED",
                                    old_val=move.verification_status,
                                    new_val=incoming_status,
                                    user=user,
                                    method="EXPLICIT_ADMIN_OVERRIDE_IMPORT",
                                    result=incoming_status,
                                    notes=f"Admin explicitly authorized overwrite of verified move {notation}.",
                                    patch_version=patch_version,
                                    source_url=source_url,
                                    move_id=move.id,
                                )
                                audit_count += 1

                        # Update fields
                        move.name = row.get("name", move.name)
                        if "startup_frames" in row and row["startup_frames"] is not None:
                            try:
                                move.startup_frames = int(row["startup_frames"])
                            except ValueError:
                                pass
                        if "block_advantage" in row and row["block_advantage"] is not None:
                            try:
                                move.block_advantage = int(row["block_advantage"])
                            except ValueError:
                                pass
                        if "hit_advantage" in row and row["hit_advantage"] is not None:
                            try:
                                move.hit_advantage = int(row["hit_advantage"])
                            except ValueError:
                                pass
                        if "damage" in row and row["damage"] is not None:
                            try:
                                move.damage = int(row["damage"])
                            except ValueError:
                                pass
                        if "hit_level" in row:
                            move.hit_level = row["hit_level"]

                        move.import_batch_id = import_batch.id
                        updated_count += 1

                        cls.log_audit_trail(
                            db=db,
                            entity_type="MOVE",
                            entity_id=move.id,
                            field_name="IMPORT_UPDATE",
                            old_val="DATABASE_PREVIOUS",
                            new_val=f"IMPORT_BATCH_{import_batch.id}",
                            user=user,
                            method="CSV_JSON_IMPORT",
                            result=move.verification_status,
                            notes=f"Updated via import from {source_name}",
                            patch_version=patch_version,
                            source_url=source_url,
                            move_id=move.id,
                        )
                        audit_count += 1
                    else:
                        # Create new Move
                        new_move = Move(
                            character_id=int(char_id),
                            name=row.get("name", notation),
                            original_notation=row.get("original_notation", notation),
                            normalized_notation=notation,
                            startup_frames=int(row["startup_frames"]) if row.get("startup_frames") is not None else None,
                            block_advantage=int(row["block_advantage"]) if row.get("block_advantage") is not None else None,
                            hit_advantage=int(row["hit_advantage"]) if row.get("hit_advantage") is not None else None,
                            damage=int(row["damage"]) if row.get("damage") is not None else None,
                            hit_level=row.get("hit_level"),
                            verification_status=incoming_status,
                            import_batch_id=import_batch.id,
                        )
                        db.add(new_move)
                        db.flush()
                        created_count += 1

                        cls.log_audit_trail(
                            db=db,
                            entity_type="MOVE",
                            entity_id=new_move.id,
                            field_name="IMPORT_CREATE",
                            old_val=None,
                            new_val=notation,
                            user=user,
                            method="CSV_JSON_IMPORT",
                            result=incoming_status,
                            notes=f"Created via import batch #{import_batch.id} ({source_name})",
                            patch_version=patch_version,
                            source_url=source_url,
                            move_id=new_move.id,
                        )
                        audit_count += 1

                elif e_type == "COMBOS":
                    char_id = int(row["character_id"])
                    title = row["title"]
                    notation = row["notation_sequence"]

                    # Strict validation check via DataValidator
                    combo_val = DataValidator.validate_combo(row, db=db)
                    critical_errors = [i for i in combo_val.issues if i.severity in ["CRITICAL", "ERROR"]]
                    if critical_errors:
                        raise ValueError(f"Row {idx+1} ({title}): {critical_errors[0].message}")


                    exist_combo = (
                        db.query(ComboRoute)
                        .filter_by(character_id=char_id, title=title)
                        .first()
                    )
                    incoming_status = row.get("verification_status", "UNVERIFIED").upper()

                    if exist_combo:
                        if exist_combo.verification_status == "VERIFIED" and incoming_status != "VERIFIED":
                            if not allow_override_verified:
                                skipped_count += 1
                                continue

                        exist_combo.notation_sequence = notation
                        exist_combo.total_damage = int(row.get("total_damage", exist_combo.total_damage))
                        exist_combo.hit_count = int(row.get("hit_count", exist_combo.hit_count))
                        exist_combo.difficulty = row.get("difficulty", exist_combo.difficulty)
                        exist_combo.combo_type = row.get("combo_type", exist_combo.combo_type)
                        updated_count += 1
                    else:
                        new_combo = ComboRoute(
                            character_id=char_id,
                            title=title,
                            notation_sequence=notation,
                            total_damage=int(row.get("total_damage", 60)),
                            hit_count=int(row.get("hit_count", 4)),
                            difficulty=row.get("difficulty", "MEDIUM"),
                            combo_type=row.get("combo_type", "MIDSCREEN"),
                            verification_status=incoming_status,
                            patch_version=patch_version,
                            source=source_name,
                        )
                        db.add(new_combo)
                        db.flush()
                        created_count += 1

            import_batch.status = "COMPLETED"
            import_batch.successful_records = created_count + updated_count
            import_batch.failed_records = skipped_count
            import_batch.completed_at = datetime.now(timezone.utc)
            db.commit()

            return ImportSummaryResponse(
                success=True,
                entity_type=e_type,
                total_submitted=len(rows),
                records_created=created_count,
                records_updated=updated_count,
                records_skipped=skipped_count,
                conflicts_logged=conflicts_count,
                audit_records_created=audit_count,
                rollback_occurred=False,
                message=f"Transaction committed successfully: {created_count} created, {updated_count} updated, {skipped_count} skipped.",
            )

        except Exception as e:
            db.rollback()
            return ImportSummaryResponse(
                success=False,
                entity_type=e_type,
                total_submitted=len(rows),
                records_created=0,
                records_updated=0,
                records_skipped=len(rows),
                conflicts_logged=0,
                audit_records_created=0,
                rollback_occurred=True,
                message=f"Atomic transaction aborted and rolled back: {str(e)}",
                error_details=str(e),
            )

    # --------------------------------------------------------------------------
    # Export System
    # --------------------------------------------------------------------------
    @classmethod
    def export_data(cls, db: Session, entity_type: str, format_type: str = "JSON") -> str:
        e_type = entity_type.upper()
        records: List[Dict[str, Any]] = []

        if e_type == "MOVES":
            moves = db.query(Move).all()
            for m in moves:
                char_slug = m.character.slug if m.character else "unknown"
                records.append({
                    "id": m.id,
                    "character_slug": char_slug,
                    "name": m.name,
                    "normalized_notation": m.normalized_notation,
                    "startup_frames": m.startup_frames,
                    "block_advantage": m.block_advantage,
                    "hit_advantage": m.hit_advantage,
                    "damage": m.damage,
                    "hit_level": m.hit_level,
                    "verification_status": m.verification_status,
                    "verification_notes": m.verification_notes,
                })
        elif e_type == "COMBOS":
            combos = db.query(ComboRoute).all()
            for c in combos:
                char_slug = c.character.slug if c.character else "unknown"
                records.append({
                    "id": c.id,
                    "character_slug": char_slug,
                    "title": c.title,
                    "notation_sequence": c.notation_sequence,
                    "total_damage": c.total_damage,
                    "hit_count": c.hit_count,
                    "difficulty": c.difficulty,
                    "combo_type": c.combo_type,
                    "target_hurtbox_class": c.target_hurtbox_class,
                    "verification_status": c.verification_status,
                    "patch_version": c.patch_version,
                    "source": c.source,
                })
        elif e_type == "STAGES":
            stages = db.query(Stage).all()
            for s in stages:
                records.append({
                    "id": s.id,
                    "slug": s.slug,
                    "name": s.name,
                    "has_walls": s.has_walls,
                    "boundary_shape": s.boundary_shape,
                    "wall_break": s.wall_break,
                    "floor_break": s.floor_break,
                    "balcony_break": s.balcony_break,
                    "special_mechanics": s.special_mechanics,
                })
        elif e_type == "SOURCES":
            sources = db.query(DataSource).all()
            for s in sources:
                records.append({
                    "id": s.id,
                    "name": s.name,
                    "base_url": s.base_url,
                    "license_type": s.license_type,
                    "attribution_text": s.attribution_text,
                    "approval_status": s.approval_status,
                })
        else:
            raise ValueError(f"Export for entity '{entity_type}' is not supported.")

        fmt = format_type.upper().strip()
        if fmt == "JSON":
            return json.dumps(records, indent=2)
        elif fmt == "CSV":
            if not records:
                return ""
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format '{format_type}'.")
