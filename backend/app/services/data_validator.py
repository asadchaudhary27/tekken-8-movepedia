import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.stage import Stage
from backend.app.models.matchup_note import MatchupNote
from backend.app.models.source import DataSource
from backend.app.models.patch import GamePatch
from backend.app.schemas.admin import (
    DataValidationIssue,
    ValidationResult,
    DatabaseAuditReport,
)


class DataValidator:
    """
    Authoritative Data Validation and Integrity Engine for Tekken 8 Data Architecture.
    Enforces relational invariants, missing-value semantics, physical gameplay bounds,
    and stage hazard compatibility rules.
    """

    VALID_HIT_LEVELS = {
        "h", "m", "l", "sm", "sl", "ub", "t", "s", "special",
        "m, h", "l, m", "h, m", "m, m", "h, h", "l, l",
        "h, m, h", "m, m, m", "l, m, m", "h, h, m", "m, h, m"
    }

    VALID_DIFFICULTIES = {"EASY", "MEDIUM", "HARD", "OPTIMAL"}
    VALID_COMBO_TYPES = {
        "MIDSCREEN", "WALL_CARRY", "WALL_COMBO", "WALL_BREAK", "FLOOR_BREAK", "BALCONY_BREAK"
    }
    VALID_VERIFICATION_STATUSES = {"VERIFIED", "UNVERIFIED", "CONFLICTING"}

    # --------------------------------------------------------------------------
    # MOVE VALIDATION
    # --------------------------------------------------------------------------
    @classmethod
    def validate_move(
        cls,
        data: Union[Dict[str, Any], Move],
        db: Optional[Session] = None,
    ) -> ValidationResult:
        issues: List[DataValidationIssue] = []

        # Normalize data access whether dict or ORM instance
        def get_val(key: str, default: Any = None) -> Any:
            if isinstance(data, dict):
                return data.get(key, default)
            return getattr(data, key, default)

        move_id = get_val("id")
        char_id = get_val("character_id")
        char_slug = get_val("character_slug")
        norm_notation = get_val("normalized_notation") or get_val("notation")
        orig_notation = get_val("original_notation")
        startup_frames = get_val("startup_frames")
        startup_raw = get_val("startup_raw")
        block_adv = get_val("block_advantage")
        block_raw = get_val("block_advantage_raw")
        hit_adv = get_val("hit_advantage")
        damage = get_val("damage")
        hit_level = get_val("hit_level")
        verification_status = get_val("verification_status", "UNVERIFIED")

        # 1. Notation check
        if not norm_notation or not str(norm_notation).strip():
            issues.append(
                DataValidationIssue(
                    entity_type="MOVE",
                    entity_id=move_id,
                    field="normalized_notation",
                    severity="CRITICAL",
                    rule="REQUIRED_NOTATION",
                    message="Move normalized_notation cannot be empty or blank.",
                    suggested_action="Provide standard Tekken 8 input notation (e.g. 'd/f+2', '1, 1, 2').",
                    context={"incoming_notation": norm_notation},
                )
            )
        else:
            notation_str = str(norm_notation).strip()
            # Check for illegal control or corrupt characters
            if any(c in notation_str for c in ["<", ">", ";", "{", "}", "\\", "`"]):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="normalized_notation",
                        severity="ERROR",
                        rule="INVALID_NOTATION_SYNTAX",
                        message=f"Move notation contains invalid syntax characters: '{notation_str}'.",
                        suggested_action="Sanitize notation to standard Tekken notation format.",
                        context={"notation": notation_str},
                    )
                )

        # 2. Character Reference check
        char_record = None
        if db is not None:
            if char_id:
                char_record = db.query(Character).filter_by(id=int(char_id)).first()
            elif char_slug:
                char_record = db.query(Character).filter_by(slug=str(char_slug)).first()

            if not char_record and (char_id or char_slug):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="character_id",
                        severity="CRITICAL",
                        rule="BROKEN_CHARACTER_REFERENCE",
                        message=f"Referenced character_id={char_id} (slug='{char_slug}') does not exist in database.",
                        suggested_action="Ensure the move references a valid character entity.",
                        context={"character_id": char_id, "character_slug": char_slug},
                    )
                )

        # 3. Startup Frames & Missing-Value Semantics
        if startup_frames is not None:
            try:
                s_val = int(startup_frames)
                if s_val <= 0:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MOVE",
                            entity_id=move_id,
                            field="startup_frames",
                            severity="CRITICAL",
                            rule="STARTUP_FRAMES_POSITIVE",
                            message=f"Invalid startup frames: {s_val}. Tekken moves cannot have startup <= 0. If unknown or inapplicable, use NULL (None), not 0.",
                            suggested_action="Set startup_frames to NULL if unknown, or provide a positive integer (e.g. 10+).",
                            context={"startup_frames": s_val},
                        )
                    )
                elif s_val > 120:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MOVE",
                            entity_id=move_id,
                            field="startup_frames",
                            severity="WARNING",
                            rule="UNUSUAL_STARTUP_BOUNDARY",
                            message=f"Unusually long startup frames: i{s_val}. Verify if this is an unblockable charge or rage art.",
                            suggested_action="Verify startup timing against Tekken 8 frame data recordings.",
                            context={"startup_frames": s_val},
                        )
                    )
            except (ValueError, TypeError):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="startup_frames",
                        severity="ERROR",
                        rule="STARTUP_NUMERIC_TYPE",
                        message=f"startup_frames must be an integer, got: {startup_frames}.",
                        suggested_action="Convert string frame data to startup_raw and provide numeric integer in startup_frames.",
                        context={"startup_frames": str(startup_frames)},
                    )
                )
        else:
            # Startup is None: Validate if proper missing-value semantics are maintained
            if not startup_raw:
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="startup_frames",
                        severity="INFO",
                        rule="MISSING_STARTUP_RECORD",
                        message="Move has no startup frame data recorded.",
                        suggested_action="Collect frame data from authorized source.",
                        context={"normalized_notation": str(norm_notation)},
                    )
                )

        # 4. Damage Validation
        if damage is not None:
            try:
                d_val = int(damage)
                if d_val < 0:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MOVE",
                            entity_id=move_id,
                            field="damage",
                            severity="ERROR",
                            rule="DAMAGE_NON_NEGATIVE",
                            message=f"Move damage cannot be negative ({d_val}).",
                            suggested_action="Correct damage value to >= 0.",
                            context={"damage": d_val},
                        )
                    )
                elif d_val == 0 and hit_level and hit_level.lower() in ["h", "m", "l"]:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MOVE",
                            entity_id=move_id,
                            field="damage",
                            severity="WARNING",
                            rule="ZERO_DAMAGE_CONTACT_MOVE",
                            message=f"Move has hit level '{hit_level}' but damage is 0.",
                            suggested_action="Verify whether this attack deals damage or is a pure stance transition/parry.",
                            context={"damage": d_val, "hit_level": hit_level},
                        )
                    )
            except (ValueError, TypeError):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="damage",
                        severity="ERROR",
                        rule="DAMAGE_NUMERIC_TYPE",
                        message=f"damage must be an integer, got: {damage}.",
                        suggested_action="Ensure damage is stored as numeric integer.",
                        context={"damage": str(damage)},
                    )
                )

        # 5. Block Advantage Range Validation
        if block_adv is not None:
            try:
                b_val = int(block_adv)
                if b_val < -120 or b_val > 120:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MOVE",
                            entity_id=move_id,
                            field="block_advantage",
                            severity="WARNING",
                            rule="BLOCK_ADVANTAGE_OUT_OF_BOUNDS",
                            message=f"Block advantage ({b_val}) is outside standard fighting game bounds (-120 to +120).",
                            suggested_action="Verify block advantage value against in-game practice mode.",
                            context={"block_advantage": b_val},
                        )
                    )
            except (ValueError, TypeError):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="block_advantage",
                        severity="ERROR",
                        rule="BLOCK_ADVANTAGE_NUMERIC_TYPE",
                        message=f"block_advantage must be an integer, got: {block_adv}.",
                        suggested_action="Store non-numeric notation (e.g. '-14~-13', 'None') in block_advantage_raw.",
                        context={"block_advantage": str(block_adv)},
                    )
                )

        # 6. Hit Level Validation
        if hit_level:
            clean_hl = str(hit_level).strip().lower()
            if clean_hl not in cls.VALID_HIT_LEVELS and not any(part in clean_hl for part in ["h", "m", "l", "ub", "t", "s"]):
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="hit_level",
                        severity="WARNING",
                        rule="UNRECOGNIZED_HIT_LEVEL",
                        message=f"Unrecognized hit level: '{hit_level}'. Expected standard notation (h, m, l, sm, sl, ub, t, s).",
                        suggested_action="Standardize hit level format.",
                        context={"hit_level": hit_level},
                    )
                )

        # 7. Verification Status Validation
        if str(verification_status).upper() not in cls.VALID_VERIFICATION_STATUSES:
            issues.append(
                DataValidationIssue(
                    entity_type="MOVE",
                    entity_id=move_id,
                    field="verification_status",
                    severity="WARNING",
                    rule="INVALID_VERIFICATION_STATUS",
                    message=f"Invalid verification status: '{verification_status}'. Must be VERIFIED, UNVERIFIED, or CONFLICTING.",
                    suggested_action="Use standard verification status constant.",
                    context={"verification_status": verification_status},
                )
            )

        # 8. Duplicate notation check within character
        if db is not None and char_record and norm_notation:
            existing_query = db.query(Move).filter_by(
                character_id=char_record.id,
                normalized_notation=str(norm_notation).strip(),
            )
            if move_id:
                existing_query = existing_query.filter(Move.id != int(move_id))
            duplicate = existing_query.first()
            if duplicate:
                issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=move_id,
                        field="normalized_notation",
                        severity="CRITICAL",
                        rule="DUPLICATE_MOVE_NOTATION",
                        message=f"Duplicate move notation: Character '{char_record.name}' already has a move with notation '{norm_notation}' (id={duplicate.id}).",
                        suggested_action="Update existing move record or disambiguate stance context.",
                        context={"existing_move_id": duplicate.id, "notation": str(norm_notation)},
                    )
                )

        errors_count = sum(1 for i in issues if i.severity in ["CRITICAL", "ERROR"])
        warnings_count = sum(1 for i in issues if i.severity == "WARNING")
        return ValidationResult(
            is_valid=(errors_count == 0),
            errors_count=errors_count,
            warnings_count=warnings_count,
            issues=issues,
        )

    # --------------------------------------------------------------------------
    # COMBO VALIDATION
    # --------------------------------------------------------------------------
    @classmethod
    def validate_combo(
        cls,
        data: Union[Dict[str, Any], ComboRoute],
        db: Optional[Session] = None,
    ) -> ValidationResult:
        issues: List[DataValidationIssue] = []

        def get_val(key: str, default: Any = None) -> Any:
            if isinstance(data, dict):
                return data.get(key, default)
            return getattr(data, key, default)

        combo_id = get_val("id")
        char_id = get_val("character_id")
        char_slug = get_val("character_slug")
        title = get_val("title")
        notation_seq = get_val("notation_sequence")
        total_dmg = get_val("total_damage")
        hit_cnt = get_val("hit_count")
        diff = get_val("difficulty", "MEDIUM")
        combo_type = get_val("combo_type", "MIDSCREEN")
        stage_id = get_val("stage_id")
        is_stage_dep = get_val("is_stage_dependent", False)
        starter_id = get_val("starter_move_id")
        alt_id = get_val("easier_alternative_id")
        uses_wall = get_val("uses_wall", False)

        # 1. Required fields
        if not title or not str(title).strip():
            issues.append(
                DataValidationIssue(
                    entity_type="COMBO",
                    entity_id=combo_id,
                    field="title",
                    severity="ERROR",
                    rule="REQUIRED_TITLE",
                    message="Combo title is required and cannot be empty.",
                    suggested_action="Provide a descriptive combo route title.",
                    context={"title": title},
                )
            )

        if not notation_seq or not str(notation_seq).strip():
            issues.append(
                DataValidationIssue(
                    entity_type="COMBO",
                    entity_id=combo_id,
                    field="notation_sequence",
                    severity="CRITICAL",
                    rule="REQUIRED_COMBO_SEQUENCE",
                    message="Combo notation_sequence is required and cannot be empty.",
                    suggested_action="Provide full input step sequence (e.g. 'd/f+2 > 4 > b+2,1 > ender').",
                    context={"notation_sequence": notation_seq},
                )
            )

        # 2. Damage & Hit count
        if total_dmg is not None:
            try:
                dmg_val = int(total_dmg)
                if dmg_val < 0:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="total_damage",
                            severity="CRITICAL",
                            rule="COMBO_DAMAGE_POSITIVE",
                            message=f"Total combo damage cannot be negative ({dmg_val}).",
                            suggested_action="Correct total_damage to positive integer.",
                            context={"total_damage": dmg_val},
                        )
                    )
                elif dmg_val == 0:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="total_damage",
                            severity="WARNING",
                            rule="COMBO_DAMAGE_ZERO",
                            message="Combo damage is 0. Combos typically deal measurable damage.",
                            suggested_action="Verify tested in-game damage total.",
                            context={"total_damage": dmg_val},
                        )
                    )
                elif dmg_val > 250:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="total_damage",
                            severity="WARNING",
                            rule="COMBO_DAMAGE_IMPLAUSIBLE",
                            message=f"Total damage ({dmg_val}) is implausibly high for Tekken 8 standard health (180 HP max).",
                            suggested_action="Verify damage scaling sum or check if multiple combos were concatenated.",
                            context={"total_damage": dmg_val},
                        )
                    )
            except (ValueError, TypeError):
                issues.append(
                    DataValidationIssue(
                        entity_type="COMBO",
                        entity_id=combo_id,
                        field="total_damage",
                        severity="ERROR",
                        rule="COMBO_DAMAGE_NUMERIC",
                        message=f"total_damage must be an integer, got: {total_dmg}.",
                        suggested_action="Cast damage to integer.",
                        context={"total_damage": str(total_dmg)},
                    )
                )

        if hit_cnt is not None:
            try:
                hit_val = int(hit_cnt)
                if hit_val < 1:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="hit_count",
                            severity="CRITICAL",
                            rule="COMBO_HIT_COUNT_POSITIVE",
                            message=f"Combo hit_count must be at least 1, got: {hit_val}.",
                            suggested_action="Provide accurate count of hits in combo sequence.",
                            context={"hit_count": hit_val},
                        )
                    )
            except (ValueError, TypeError):
                issues.append(
                    DataValidationIssue(
                        entity_type="COMBO",
                        entity_id=combo_id,
                        field="hit_count",
                        severity="ERROR",
                        rule="COMBO_HIT_COUNT_NUMERIC",
                        message=f"hit_count must be an integer, got: {hit_cnt}.",
                        suggested_action="Cast hit count to integer.",
                        context={"hit_count": str(hit_cnt)},
                    )
                )

        # 3. Enumeration check
        if diff and str(diff).upper() not in cls.VALID_DIFFICULTIES:
            issues.append(
                DataValidationIssue(
                    entity_type="COMBO",
                    entity_id=combo_id,
                    field="difficulty",
                    severity="WARNING",
                    rule="INVALID_DIFFICULTY_ENUM",
                    message=f"Invalid combo difficulty: '{diff}'. Expected EASY, MEDIUM, HARD, or OPTIMAL.",
                    suggested_action="Use standard difficulty level.",
                    context={"difficulty": diff},
                )
            )

        clean_combo_type = str(combo_type).upper() if combo_type else "MIDSCREEN"
        if clean_combo_type not in cls.VALID_COMBO_TYPES:
            issues.append(
                DataValidationIssue(
                    entity_type="COMBO",
                    entity_id=combo_id,
                    field="combo_type",
                    severity="WARNING",
                    rule="INVALID_COMBO_TYPE_ENUM",
                    message=f"Invalid combo_type: '{combo_type}'. Expected MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK.",
                    suggested_action="Map to valid combo category.",
                    context={"combo_type": combo_type},
                )
            )

        # 4. Cross-Entity Character & Starter Move Verification
        char_record = None
        if db is not None:
            if char_id:
                char_record = db.query(Character).filter_by(id=int(char_id)).first()
            elif char_slug:
                char_record = db.query(Character).filter_by(slug=str(char_slug)).first()

            if not char_record and (char_id or char_slug):
                issues.append(
                    DataValidationIssue(
                        entity_type="COMBO",
                        entity_id=combo_id,
                        field="character_id",
                        severity="CRITICAL",
                        rule="BROKEN_CHARACTER_REFERENCE",
                        message=f"Referenced character_id={char_id} (slug='{char_slug}') does not exist.",
                        suggested_action="Associate combo with an existing character entity.",
                        context={"character_id": char_id, "character_slug": char_slug},
                    )
                )

            # CRITICAL RELATIONAL INTEGRITY RULE: Starter Move Character Mismatch
            if starter_id and char_record:
                starter_move = db.query(Move).filter_by(id=int(starter_id)).first()
                if not starter_move:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="starter_move_id",
                            severity="CRITICAL",
                            rule="BROKEN_STARTER_MOVE_REFERENCE",
                            message=f"starter_move_id={starter_id} does not exist in moves database.",
                            suggested_action="Remove or correct the starter_move_id.",
                            context={"starter_move_id": starter_id},
                        )
                    )
                elif starter_move.character_id != char_record.id:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="starter_move_id",
                            severity="CRITICAL",
                            rule="STARTER_CHARACTER_MISMATCH",
                            message=(
                                f"RELATIONAL INTEGRITY ERROR: Starter move '{starter_move.name or starter_move.normalized_notation}' "
                                f"belongs to character_id={starter_move.character_id} ({starter_move.character.name if starter_move.character else 'Unknown'}), "
                                f"but combo belongs to character_id={char_record.id} ({char_record.name})."
                            ),
                            suggested_action="Assign a starter move that belongs to the same character as the combo.",
                            context={
                                "combo_character_id": char_record.id,
                                "combo_character_name": char_record.name,
                                "starter_move_id": starter_move.id,
                                "starter_move_character_id": starter_move.character_id,
                            },
                        )
                    )

            # 5. Stage Compatibility Invariant
            if stage_id:
                stage_record = db.query(Stage).filter_by(id=int(stage_id)).first()
                if not stage_record:
                    issues.append(
                        DataValidationIssue(
                            entity_type="COMBO",
                            entity_id=combo_id,
                            field="stage_id",
                            severity="ERROR",
                            rule="BROKEN_STAGE_REFERENCE",
                            message=f"Referenced stage_id={stage_id} does not exist in stages database.",
                            suggested_action="Verify or remove stage_id reference.",
                            context={"stage_id": stage_id},
                        )
                    )
                else:
                    # Invariant: Wall combo or wall route on wall-less stage
                    if (clean_combo_type in ["WALL_COMBO", "WALL_BREAK", "WALL_CARRY"] or uses_wall) and not stage_record.has_walls:
                        issues.append(
                            DataValidationIssue(
                                entity_type="COMBO",
                                entity_id=combo_id,
                                field="stage_id",
                                severity="CRITICAL",
                                rule="STAGE_HAZARD_CONFLICT",
                                message=(
                                    f"CONFLICT: Combo requires wall ({clean_combo_type}), but stage '{stage_record.name}' "
                                    f"is an infinite arena without walls (has_walls=False)."
                                ),
                                suggested_action="Change stage reference to a walled arena or update combo_type to MIDSCREEN.",
                                context={"stage_id": stage_record.id, "stage_name": stage_record.name, "combo_type": clean_combo_type},
                            )
                        )

                    # Invariant: Wall Break on non-wall-break stage
                    if clean_combo_type == "WALL_BREAK" and not (stage_record.wall_break or stage_record.wall_blast):
                        issues.append(
                            DataValidationIssue(
                                entity_type="COMBO",
                                entity_id=combo_id,
                                field="stage_id",
                                severity="ERROR",
                                rule="STAGE_HAZARD_CONFLICT",
                                message=f"CONFLICT: Combo is WALL_BREAK, but stage '{stage_record.name}' does not have wall breaks or blasts.",
                                suggested_action="Select a stage with verified wall breaks (e.g. Ortiz Farm, Rebel Hangar).",
                                context={"stage_id": stage_record.id, "stage_name": stage_record.name},
                            )
                        )

                    # Invariant: Floor Break on non-floor-break stage
                    if clean_combo_type == "FLOOR_BREAK" and not (stage_record.floor_break or stage_record.floor_blast):
                        issues.append(
                            DataValidationIssue(
                                entity_type="COMBO",
                                entity_id=combo_id,
                                field="stage_id",
                                severity="ERROR",
                                rule="STAGE_HAZARD_CONFLICT",
                                message=f"CONFLICT: Combo is FLOOR_BREAK, but stage '{stage_record.name}' does not have floor breaks or blasts.",
                                suggested_action="Select a stage with floor breaks or blasts (e.g. Descent into Subconscious, Sanctum, Into the Stratosphere).",
                                context={"stage_id": stage_record.id, "stage_name": stage_record.name},
                            )
                        )

                    # Invariant: Balcony Break on non-balcony stage
                    if clean_combo_type == "BALCONY_BREAK" and not stage_record.balcony_break:
                        issues.append(
                            DataValidationIssue(
                                entity_type="COMBO",
                                entity_id=combo_id,
                                field="stage_id",
                                severity="ERROR",
                                rule="STAGE_HAZARD_CONFLICT",
                                message=f"CONFLICT: Combo is BALCONY_BREAK, but stage '{stage_record.name}' does not have balcony breaks (balcony_break=False).",
                                suggested_action="Select a stage with balcony breaks (e.g. Arena Underground).",
                                context={"stage_id": stage_record.id, "stage_name": stage_record.name},
                            )
                        )

        # 6. Easier alternative reference checks
        if alt_id and combo_id and int(alt_id) == int(combo_id):
            issues.append(
                DataValidationIssue(
                    entity_type="COMBO",
                    entity_id=combo_id,
                    field="easier_alternative_id",
                    severity="CRITICAL",
                    rule="SELF_REFERENTIAL_ALTERNATIVE",
                    message="Combo cannot list itself as its own easier alternative.",
                    suggested_action="Point to a distinct lower-difficulty route or leave NULL.",
                    context={"combo_id": combo_id, "easier_alternative_id": alt_id},
                )
            )
        elif alt_id and db is not None and char_record:
            alt_combo = db.query(ComboRoute).filter_by(id=int(alt_id)).first()
            if not alt_combo:
                issues.append(
                    DataValidationIssue(
                        entity_type="COMBO",
                        entity_id=combo_id,
                        field="easier_alternative_id",
                        severity="ERROR",
                        rule="BROKEN_ALTERNATIVE_COMBO_REFERENCE",
                        message=f"easier_alternative_id={alt_id} does not exist in combo routes.",
                        suggested_action="Update or remove easier_alternative_id reference.",
                        context={"easier_alternative_id": alt_id},
                    )
                )
            elif alt_combo.character_id != char_record.id:
                issues.append(
                    DataValidationIssue(
                        entity_type="COMBO",
                        entity_id=combo_id,
                        field="easier_alternative_id",
                        severity="CRITICAL",
                        rule="ALTERNATIVE_CHARACTER_MISMATCH",
                        message=f"Alternative combo id={alt_id} belongs to a different character ({alt_combo.character_id}).",
                        suggested_action="Link to an alternative route belonging to the same character.",
                        context={"combo_char_id": char_record.id, "alt_char_id": alt_combo.character_id},
                    )
                )


        errors_count = sum(1 for i in issues if i.severity in ["CRITICAL", "ERROR"])
        warnings_count = sum(1 for i in issues if i.severity == "WARNING")
        return ValidationResult(
            is_valid=(errors_count == 0),
            errors_count=errors_count,
            warnings_count=warnings_count,
            issues=issues,
        )

    # --------------------------------------------------------------------------
    # STAGE VALIDATION
    # --------------------------------------------------------------------------
    @classmethod
    def validate_stage(
        cls,
        data: Union[Dict[str, Any], Stage],
        db: Optional[Session] = None,
    ) -> ValidationResult:
        issues: List[DataValidationIssue] = []

        def get_val(key: str, default: Any = None) -> Any:
            if isinstance(data, dict):
                return data.get(key, default)
            return getattr(data, key, default)

        stage_id = get_val("id")
        slug = get_val("slug")
        name = get_val("name")
        has_walls = get_val("has_walls", True)
        wall_break = get_val("wall_break", False)
        wall_blast = get_val("wall_blast", False)
        wall_bound = get_val("wall_bound", False)
        hard_wall_break = get_val("hard_wall_break", False)
        total_sections = get_val("total_sections", 1)

        if not slug or not str(slug).strip():
            issues.append(
                DataValidationIssue(
                    entity_type="STAGE",
                    entity_id=stage_id,
                    field="slug",
                    severity="CRITICAL",
                    rule="REQUIRED_STAGE_SLUG",
                    message="Stage slug is required and cannot be empty.",
                    suggested_action="Provide unique kebab-case slug (e.g. 'arena-underground').",
                    context={"slug": slug},
                )
            )

        if not name or not str(name).strip():
            issues.append(
                DataValidationIssue(
                    entity_type="STAGE",
                    entity_id=stage_id,
                    field="name",
                    severity="CRITICAL",
                    rule="REQUIRED_STAGE_NAME",
                    message="Stage name is required and cannot be empty.",
                    suggested_action="Provide official Tekken 8 stage name.",
                    context={"name": name},
                )
            )

        # Invariant: Infinite stages cannot support wall hazards
        if not has_walls:
            if wall_break or wall_blast or wall_bound or hard_wall_break:
                issues.append(
                    DataValidationIssue(
                        entity_type="STAGE",
                        entity_id=stage_id,
                        field="has_walls",
                        severity="CRITICAL",
                        rule="INFINITE_STAGE_HAS_WALL_HAZARDS",
                        message=f"CONFLICT: Stage '{name}' has has_walls=False, but enables wall hazards (break={wall_break}, blast={wall_blast}).",
                        suggested_action="Disable wall hazard flags for infinite/wall-less stages, or set has_walls=True.",
                        context={"has_walls": has_walls, "wall_break": wall_break, "wall_blast": wall_blast},
                    )
                )

        if total_sections is not None and int(total_sections) < 1:
            issues.append(
                DataValidationIssue(
                    entity_type="STAGE",
                    entity_id=stage_id,
                    field="total_sections",
                    severity="ERROR",
                    rule="STAGE_SECTIONS_MINIMUM",
                    message=f"Stage must have at least 1 section, got: {total_sections}.",
                    suggested_action="Set total_sections >= 1.",
                    context={"total_sections": total_sections},
                )
            )

        errors_count = sum(1 for i in issues if i.severity in ["CRITICAL", "ERROR"])
        warnings_count = sum(1 for i in issues if i.severity == "WARNING")
        return ValidationResult(
            is_valid=(errors_count == 0),
            errors_count=errors_count,
            warnings_count=warnings_count,
            issues=issues,
        )

    # --------------------------------------------------------------------------
    # MATCHUP NOTE VALIDATION
    # --------------------------------------------------------------------------
    @classmethod
    def validate_matchup_note(
        cls,
        data: Union[Dict[str, Any], MatchupNote],
        db: Optional[Session] = None,
    ) -> ValidationResult:
        issues: List[DataValidationIssue] = []

        def get_val(key: str, default: Any = None) -> Any:
            if isinstance(data, dict):
                return data.get(key, default)
            return getattr(data, key, default)

        note_id = get_val("id")
        p1_id = get_val("player_character_id")
        p2_id = get_val("opponent_character_id")
        conf_score = get_val("confidence_score", 50)
        rating = get_val("rating", "EVEN")

        if p1_id and p2_id and int(p1_id) == int(p2_id):
            issues.append(
                DataValidationIssue(
                    entity_type="MATCHUP_NOTE",
                    entity_id=note_id,
                    field="opponent_character_id",
                    severity="CRITICAL",
                    rule="MIRROR_MATCHUP_NOTE_CONFLICT",
                    message=f"Mirror matchup note conflict: player_character_id and opponent_character_id are both {p1_id}.",
                    suggested_action="Assign distinct player and opponent character IDs.",
                    context={"player_id": p1_id, "opponent_id": p2_id},
                )
            )

        if conf_score is not None:
            try:
                cs = int(conf_score)
                if cs < 0 or cs > 100:
                    issues.append(
                        DataValidationIssue(
                            entity_type="MATCHUP_NOTE",
                            entity_id=note_id,
                            field="confidence_score",
                            severity="ERROR",
                            rule="CONFIDENCE_SCORE_RANGE",
                            message=f"Confidence score must be between 0 and 100, got: {cs}.",
                            suggested_action="Clamp confidence score to range 0..100.",
                            context={"confidence_score": cs},
                        )
                    )
            except (ValueError, TypeError):
                pass

        errors_count = sum(1 for i in issues if i.severity in ["CRITICAL", "ERROR"])
        warnings_count = sum(1 for i in issues if i.severity == "WARNING")
        return ValidationResult(
            is_valid=(errors_count == 0),
            errors_count=errors_count,
            warnings_count=warnings_count,
            issues=issues,
        )

    # --------------------------------------------------------------------------
    # FULL DATABASE INTEGRITY AUDIT SCAN
    # --------------------------------------------------------------------------
    @classmethod
    def audit_entire_database(cls, db: Session) -> DatabaseAuditReport:
        """
        Executes an exhaustive, non-destructive diagnostic scan of the active database.
        Checks foreign key integrity, cross-entity invariants, physical fighting game bounds,
        missing-value semantics, and hazard consistency.
        """
        all_issues: List[DataValidationIssue] = []

        total_characters = db.query(Character).count()
        total_moves = db.query(Move).count()
        total_combos = db.query(ComboRoute).count()
        total_stages = db.query(Stage).count()

        # 1. Audit all Stages
        stages = db.query(Stage).all()
        for s in stages:
            res = cls.validate_stage(s, db=db)
            all_issues.extend(res.issues)

        # 2. Audit all Moves
        moves = db.query(Move).all()
        valid_char_ids = {c.id for c in db.query(Character.id).all()}

        null_startup_count = 0
        conditional_startup_count = 0
        verified_moves_count = 0
        unverified_moves_count = 0

        for m in moves:
            # Foreign key check
            if m.character_id not in valid_char_ids:
                all_issues.append(
                    DataValidationIssue(
                        entity_type="MOVE",
                        entity_id=m.id,
                        field="character_id",
                        severity="CRITICAL",
                        rule="ORPHANED_FOREIGN_KEY",
                        message=f"Move id={m.id} ('{m.normalized_notation}') references nonexistent character_id={m.character_id}.",
                        suggested_action="Reassign to valid character or delete orphaned record.",
                        context={"move_id": m.id, "character_id": m.character_id},
                    )
                )

            # Move validation
            res = cls.validate_move(m, db=db)
            # Filter duplicate warnings if already evaluated
            all_issues.extend(res.issues)

            # Missing-value metrics
            if m.startup_frames is None:
                null_startup_count += 1
                if m.startup_raw and any(k in m.startup_raw for k in ["~", "c", "g", "N/A"]):
                    conditional_startup_count += 1
            if m.verification_status == "VERIFIED":
                verified_moves_count += 1
            else:
                unverified_moves_count += 1

        # 3. Audit all Combos
        combos = db.query(ComboRoute).all()
        for c in combos:
            res = cls.validate_combo(c, db=db)
            all_issues.extend(res.issues)

        # 4. Audit all Matchup Notes
        notes = db.query(MatchupNote).all()
        for n in notes:
            res = cls.validate_matchup_note(n, db=db)
            all_issues.extend(res.issues)

        # 5. Calculate Metrics and Health Score
        critical_count = sum(1 for i in all_issues if i.severity == "CRITICAL")
        error_count = sum(1 for i in all_issues if i.severity == "ERROR")
        warning_count = sum(1 for i in all_issues if i.severity == "WARNING")
        info_count = sum(1 for i in all_issues if i.severity == "INFO")

        # Health score formula: 100 - (critical * 5) - (error * 2) - (warning * 0.5)
        # Clamped between 0 and 100
        score = 100.0 - (critical_count * 5.0) - (error_count * 2.0) - (warning_count * 0.5)
        health_score = max(0.0, min(100.0, round(score, 1)))

        recommendations: List[str] = []
        if critical_count > 0:
            recommendations.append(f"Resolve {critical_count} critical integrity errors (starter mismatches, broken FKs, or negative frame data) immediately.")
        if error_count > 0:
            recommendations.append(f"Fix {error_count} error issues to restore full relational consistency.")
        if null_startup_count > conditional_startup_count:
            recommendations.append(f"{null_startup_count - conditional_startup_count} moves have unrecorded startup frames; run frame data ingestion pipeline.")
        if unverified_moves_count > 0:
            recommendations.append(f"{unverified_moves_count} moves remain unverified; schedule admin lab verification sessions.")
        if not recommendations:
            recommendations.append("Database architecture is in optimal health. All relational invariants and frame boundaries are respected.")

        missing_summary = {
            "total_moves_scanned": total_moves,
            "moves_missing_numeric_startup": null_startup_count,
            "moves_with_conditional_startup_raw": conditional_startup_count,
            "verified_moves_count": verified_moves_count,
            "unverified_moves_count": unverified_moves_count,
            "total_combos_scanned": total_combos,
            "total_stages_scanned": total_stages,
        }

        return DatabaseAuditReport(
            timestamp=datetime.now(timezone.utc),
            total_characters=total_characters,
            total_moves=total_moves,
            total_combos=total_combos,
            total_stages=total_stages,
            health_score=health_score,
            is_healthy=(critical_count == 0 and error_count == 0),
            critical_issues_count=critical_count,
            error_issues_count=error_count,
            warning_issues_count=warning_count,
            info_issues_count=info_count,
            issues=all_issues,
            missing_value_summary=missing_summary,
            recommendations=recommendations,
        )
