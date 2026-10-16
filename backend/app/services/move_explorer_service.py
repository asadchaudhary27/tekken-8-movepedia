from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from backend.app.models.move import Move
from backend.app.models.character import Character
from backend.app.models.move_property import MoveProperty
from backend.app.models.patch import GamePatch
from backend.app.models.source import DataSource
from backend.app.schemas.move import (
    MoveResponse,
    MovePropertySchema,
    MoveInputSchema,
    MoveSummaryStats,
)


class MoveExplorerService:
    """
    Authoritative service for Tekken 8 Move Explorer and verified frame data.
    Enforces strict field separation (frame advantage != animation != recovery != startup),
    explicit field states (VERIFIED, CONDITIONAL, NOT_APPLICABLE, UNVERIFIED, UNKNOWN),
    and verified punish calculations grounded in Tekken 8 frame mechanics.
    """

    @staticmethod
    def enrich_move(move: Move) -> MoveResponse:
        char_name = move.character.name if move.character else None
        char_slug = move.character.slug if move.character else None

        patch_ver = move.patch.version_number if move.patch else "3.00.02"
        src_name = "wavu_wiki"
        src_url = "https://wavu.wiki/"
        if move.import_batch and move.import_batch.source:
            src_name = move.import_batch.source.name
            src_url = move.import_batch.source.base_url

        props = move.properties or []
        prop_types = [p.property_type.lower() for p in props]

        is_heat_engager = any("heat-engager" in pt or "heat_engager" in pt for pt in prop_types)
        is_power_crush = any("power-crush" in pt or "power_crush" in pt for pt in prop_types)
        is_homing = any("homing" in pt for pt in prop_types)
        is_tornado = any("tornado" in pt for pt in prop_types)
        is_ch_launcher = any("counter-hit-launcher" in pt or "ch-launcher" in pt for pt in prop_types)
        is_stance = (move.hit_level or "").lower() == "s" or any("stance" in pt for pt in prop_types)
        has_pushback = any("pushback" in pt for pt in prop_types)
        has_extreme_pushback = any("extreme-pushback" in pt for pt in prop_types)

        # Hit Level Classification
        raw_hl = (move.hit_level or "").lower()
        if raw_hl == "s" or is_stance:
            hit_level_type = "STANCE"
        elif raw_hl == "t" or any("throw" in pt for pt in prop_types):
            hit_level_type = "THROW"
        elif "sm" in raw_hl:
            hit_level_type = "SPECIAL_MID"
        elif "l" in raw_hl:
            hit_level_type = "LOW"
        elif "m" in raw_hl:
            hit_level_type = "MID"
        elif "h" in raw_hl:
            hit_level_type = "HIGH"
        else:
            hit_level_type = "UNKNOWN"

        # Explicit Frame State Analysis
        ba_raw = move.block_advantage_raw or ""
        su_raw = move.startup_raw or ""
        ha_raw = move.hit_advantage_raw or ""
        ch_raw = move.ch_advantage_raw or ""

        is_conditional = (
            "~" in ba_raw
            or "~" in su_raw
            or "c" in ha_raw
            or "g" in ba_raw
            or "a" in ha_raw
            or "k" in ha_raw
        )
        ba = move.block_advantage

        if is_stance or ba_raw.upper() == "N/A":
            frame_state_type = "NOT_APPLICABLE"
            block_safety = "NOT_APPLICABLE"
            punish_recommendation = "N/A (Stance / Technical Transition)"
            punish_min = None
            is_launch_punish = False
            is_plus = False
        elif ba is None and not ba_raw:
            frame_state_type = "UNKNOWN"
            block_safety = "UNKNOWN"
            punish_recommendation = "Unknown (Frame Data Incomplete)"
            punish_min = None
            is_launch_punish = False
            is_plus = False
        else:
            if is_conditional:
                frame_state_type = "CONDITIONAL"
            elif move.verification_status == "VERIFIED":
                frame_state_type = "VERIFIED"
            else:
                frame_state_type = move.verification_status or "UNVERIFIED"


            # Block Safety and Verified Punish Logic
            if ba is None:
                block_safety = "UNKNOWN"
                punish_recommendation = f"Conditional ({ba_raw})" if ba_raw else "Unknown"
                punish_min = None
                is_launch_punish = False
                is_plus = False
            elif ba >= 1:
                block_safety = "PLUS"
                is_plus = True
                is_launch_punish = False
                punish_min = None
                punish_recommendation = f"Plus on Block (+{ba}) — Frame Trap Advantage"
            elif ba == 0:
                block_safety = "SAFE"
                is_plus = False
                is_launch_punish = False
                punish_min = None
                punish_recommendation = "Neutral on Block (±0) — Even Frame Reset"
            elif -9 <= ba <= -1:
                block_safety = "SAFE"
                is_plus = False
                is_launch_punish = False
                punish_min = None
                punish_recommendation = f"Safe on Block ({ba}) — Opponent Turn"
            elif -14 <= ba <= -10:
                block_safety = "UNSAFE"
                is_plus = False
                is_launch_punish = False
                punish_min = abs(ba)
                if has_extreme_pushback:
                    punish_recommendation = f"Unsafe ({ba}) [Extreme Pushback: Range Dependent]"
                elif has_pushback:
                    punish_recommendation = f"Standing i{abs(ba)} Punish (Moderate Pushback)"
                elif ba == -10:
                    punish_recommendation = "Standing i10 Punishable (Standard 1, 1,2 Jab String)"
                elif ba == -11:
                    punish_recommendation = "Standing i11 Punishable (Fast String Punish)"
                elif ba == -12:
                    punish_recommendation = "Standing i12 Punishable (Medium 2-hit Punish)"
                elif ba == -13:
                    punish_recommendation = "Standing i13 Punishable (Twin Pistons / Stiff Punish)"
                elif ba == -14:
                    punish_recommendation = "Standing i14 Punishable (Heavy Knockdown Punish)"
                else:
                    punish_recommendation = f"Standing i{abs(ba)} Punishable"
            else:  # ba <= -15
                block_safety = "LAUNCH_PUNISH"
                is_plus = False
                is_launch_punish = True
                punish_min = 15
                if has_extreme_pushback:
                    punish_recommendation = f"Launch Punishable ({ba}) [Pushback: Long-Range Launcher Required]"
                else:
                    punish_recommendation = f"Launch Punishable ({ba}: Full Hopkick / Upper Juggle Launch)"

        # Append crouch / guard break conditional context
        conditional_notes = []
        if "c" in ha_raw or "c" in ba_raw:
            conditional_notes.append("Recovers in Crouch (While-Standing / WS advantage applies)")
        if "g" in ba_raw:
            conditional_notes.append("Guard Break Stun (Opponent cannot interrupt follow-up)")
        if "a" in ha_raw:
            conditional_notes.append("Airborne Launch State on Hit")
        if "k" in ha_raw:
            conditional_notes.append("Knockdown / Wall Splat State on Hit")
        if "~" in su_raw:
            conditional_notes.append(f"Variable Startup Active Window ({su_raw})")
        if "~" in ba_raw:
            conditional_notes.append(f"Variable Block Advantage ({ba_raw})")

        # Tracking Property
        if is_homing:
            tracking_property = "HOMING"
        elif any("track-left" in pt for pt in prop_types):
            tracking_property = "TRACKS_LEFT"
        elif any("track-right" in pt for pt in prop_types):
            tracking_property = "TRACKS_RIGHT"
        else:
            tracking_property = "LINEAR"

        # Strategic Defensive Advice
        def_notes = []
        if hit_level_type == "HIGH":
            def_notes.append("High attack: Duck under or High-Crush for full launch punish.")
        elif hit_level_type == "MID":
            def_notes.append("Mid attack: Hits ducking opponents. Must be guarded standing.")
        elif hit_level_type == "LOW":
            def_notes.append("Low attack: Must be blocked crouching or Low-Parried.")
        elif hit_level_type == "THROW":
            def_notes.append("Command/Standard Throw: Duck or break on reaction.")
        elif hit_level_type == "SPECIAL_MID":
            def_notes.append("Special Mid: Guardable standing or crouching.")

        if is_homing:
            def_notes.append("Homing: Do not attempt to side-step.")
        elif tracking_property == "LINEAR":
            def_notes.append("Linear: Can be side-stepped or walked.")

        if is_power_crush:
            def_notes.append("Power Crush: Absorbs High/Mid hits; interrupted by Lows and Throws.")
        if is_heat_engager:
            def_notes.append("Heat Engager: Triggers Heat activation and dash on hit.")
        if is_tornado:
            def_notes.append("Tornado: Causes tailspin bound in juggles.")

        # Stance Awareness & Classification
        orig_not = move.original_notation or ""
        norm_not = move.normalized_notation or ""
        name_lower = (move.name or "").lower()
        stance_ctx = move.stance_context or ""

        # Stance transition (enters stance): e.g. ~F, ~B, ~D, ~U, property, or context
        is_stance_trans = (
            "~f" in orig_not.lower()
            or "~b" in orig_not.lower()
            or "~d" in orig_not.lower()
            or "~u" in orig_not.lower()
            or any("transition" in pt for pt in prop_types)
        )
        # Stance attack (executed out of stance):
        stance_prefixes = [
            "ZEN", "HBS", "MCD", "WAVU", "SNEAK", "FC", "WS", "LCT", "ALB", "WR", 
            "AOP", "RDS", "CD", "DES", "RSS", "LFF", "RFF", "FLA", "BOK", "SIT", "RLX"
        ]
        is_from_st = False
        detected_stance = stance_ctx or None
        for sp in stance_prefixes:
            if orig_not.upper().startswith(f"{sp} ") or orig_not.upper().startswith(f"{sp}+"):
                is_from_st = True
                if not detected_stance:
                    detected_stance = sp
                break

        # Pushback Warning
        has_pb = has_pushback or has_extreme_pushback or any(kw in orig_not.lower() for kw in ["d,df,f+2", "f,f+2"])
        pb_warning = None
        if has_extreme_pushback or "deathfist" in name_lower or "phoenix smasher" in name_lower:
            pb_warning = "Extreme pushback on block: standard Range 1 i10 jab punishes will whiff. Use character-specific long-range punishers (e.g. f+1+2 or dash-in WS)."
        elif has_pushback or "demon paw" in name_lower:
            pb_warning = "Moderate pushback on block: spacing dependent; deep block required for standard jab punishes."

        # Punish Window Calculation
        punish_win_frames = abs(ba) if (ba is not None and ba <= -10) else None
        if is_stance or frame_state_type == "NOT_APPLICABLE":
            punish_win_type = "NOT_APPLICABLE"
        elif ba is None:
            punish_win_type = "UNKNOWN"
        elif ba >= 1:
            punish_win_type = "PLUS"
        elif ba == 0:
            punish_win_type = "NEUTRAL"
        elif -9 <= ba <= -1:
            punish_win_type = "SAFE"
        elif -14 <= ba <= -10:
            if hit_level_type == "LOW" or "c" in ba_raw:
                punish_win_type = "CROUCH_PUNISH"
            else:
                punish_win_type = "STANDING_PUNISH"
        else:  # ba <= -15
            if hit_level_type == "LOW" or "c" in ba_raw:
                punish_win_type = "WS_LAUNCH_PUNISH"
            else:
                punish_win_type = "LAUNCH_PUNISH"

        return MoveResponse(
            id=move.id,
            character_id=move.character_id,
            character_name=char_name,
            character_slug=char_slug,
            stable_source_id=move.stable_source_id,
            name=move.name,
            original_notation=move.original_notation,
            normalized_notation=move.normalized_notation,
            startup_frames=move.startup_frames,
            startup_raw=move.startup_raw,
            block_advantage=move.block_advantage,
            block_advantage_raw=move.block_advantage_raw,
            hit_advantage=move.hit_advantage,
            hit_advantage_raw=move.hit_advantage_raw,
            ch_advantage=move.ch_advantage,
            ch_advantage_raw=move.ch_advantage_raw,
            damage=move.damage,
            damage_raw=move.damage_raw,
            hit_level=move.hit_level,
            stance_context=move.stance_context,
            verification_status=move.verification_status,
            verification_notes=move.verification_notes,
            hit_level_type=hit_level_type,
            block_safety=block_safety,
            punish_recommendation=punish_recommendation,
            punish_startup_min=punish_min,
            punish_window_frames=punish_win_frames,
            punish_window_type=punish_win_type,
            has_pushback=has_pb,
            pushback_warning=pb_warning,
            is_launch_punishable=is_launch_punish,
            is_plus_on_block=is_plus,
            is_homing=is_homing,
            is_tornado=is_tornado,
            is_heat_engager=is_heat_engager,
            is_power_crush=is_power_crush,
            is_counter_hit_launcher=is_ch_launcher,
            is_stance_move=is_stance,
            is_stance_transition=is_stance_trans,
            is_from_stance=is_from_st,
            stance_name=detected_stance,
            transition_stance=move.stance_context,
            recovery_frames=None,
            recovery_raw=None,
            tracking_property=tracking_property,
            defensive_response=" • ".join(def_notes) if def_notes else None,
            conditional_notes=" • ".join(conditional_notes) if conditional_notes else None,
            frame_state_type=frame_state_type,
            patch_version=patch_ver,
            source_name=src_name,
            source_url=src_url,

            last_verified_date=move.updated_at or move.created_at,
            properties=[
                MovePropertySchema(property_type=p.property_type, value=p.value)
                for p in props
            ],
            inputs=[
                MoveInputSchema(
                    sequence_index=i.sequence_index,
                    direction_code=i.direction_code,
                    buttons_raw=i.buttons_raw,
                    is_simultaneous=i.is_simultaneous,
                    is_hold=i.is_hold,
                    is_just_frame=i.is_just_frame,
                    stance_name=i.stance_name,
                )
                for i in (move.inputs or [])
            ],
            created_at=move.created_at,
            updated_at=move.updated_at,
        )

    @classmethod
    def filter_moves(
        cls,
        db: Session,
        character_id: Optional[int] = None,
        character_slug: Optional[str] = None,
        hit_level: Optional[str] = None,
        startup_min: Optional[int] = None,
        startup_max: Optional[int] = None,
        block_safety: Optional[str] = None,
        punishability: Optional[str] = None,
        property_type: Optional[str] = None,
        stance: Optional[str] = None,
        verification_status: Optional[str] = None,
        patch_version: Optional[str] = None,
        query_str: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[MoveResponse], int]:
        query = db.query(Move)

        # Character resolution
        if character_id:
            query = query.filter(Move.character_id == character_id)
        elif character_slug:
            char = db.query(Character).filter(Character.slug == character_slug.lower()).first()
            if char:
                query = query.filter(Move.character_id == char.id)
            else:
                return [], 0

        # Hit Level
        if hit_level and hit_level.upper() != "ALL":
            hl_clean = hit_level.lower().strip()
            if hl_clean in ["high", "h"]:
                query = query.filter(Move.hit_level.ilike("%h%"))
            elif hl_clean in ["mid", "m"]:
                query = query.filter(Move.hit_level.ilike("%m%"))
            elif hl_clean in ["low", "l"]:
                query = query.filter(Move.hit_level.ilike("%l%"))
            elif hl_clean in ["sm", "special_mid", "special mid"]:
                query = query.filter(Move.hit_level.ilike("%sm%"))
            elif hl_clean in ["throw", "t"]:
                query = query.filter(or_(Move.hit_level.ilike("%t%"), Move.properties.any(MoveProperty.property_type.ilike("%throw%"))))
            elif hl_clean in ["stance", "s"]:
                query = query.filter(or_(Move.hit_level == "s", Move.stance_context.isnot(None)))

        # Startup frame range
        if startup_min is not None:
            query = query.filter(Move.startup_frames >= startup_min)
        if startup_max is not None:
            query = query.filter(Move.startup_frames <= startup_max)

        # Block Safety
        if block_safety and block_safety.upper() != "ALL":
            bs = block_safety.upper()
            if bs == "NOT_APPLICABLE":
                query = query.filter(
                    or_(
                        Move.hit_level == "s",
                        Move.properties.any(MoveProperty.property_type.ilike("%stance%")),
                        Move.block_advantage_raw == "N/A",
                    )
                )
            else:
                # Exclude stance transitions from concrete frame advantage categories
                query = query.filter(
                    and_(
                        Move.hit_level != "s",
                        ~Move.properties.any(MoveProperty.property_type.ilike("%stance%")),
                        or_(Move.block_advantage_raw.is_(None), Move.block_advantage_raw != "N/A"),
                    )
                )
                if bs == "SAFE":
                    query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage >= -9, Move.block_advantage <= 0))
                elif bs == "UNSAFE":
                    query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage <= -10, Move.block_advantage >= -14))
                elif bs == "LAUNCH_PUNISH":
                    query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage <= -15))
                elif bs == "PLUS":
                    query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage >= 1))

        # Punishability
        if punishability and punishability.upper() != "ALL":
            pb = punishability.upper()
            if pb == "SAFE":
                query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage >= -9))
            elif pb == "PUNISHABLE_10":
                query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage <= -10, Move.block_advantage >= -11))
            elif pb == "PUNISHABLE_12":
                query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage <= -12, Move.block_advantage >= -13))
            elif pb == "PUNISHABLE_14":
                query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage == -14))
            elif pb == "LAUNCH_PUNISHABLE":
                query = query.filter(and_(Move.block_advantage.isnot(None), Move.block_advantage <= -15))

        # Property type
        if property_type and property_type.upper() != "ALL":
            pt = property_type.lower().replace("_", "-")
            query = query.filter(Move.properties.any(MoveProperty.property_type.ilike(f"%{pt}%")))

        # Stance
        if stance and stance.upper() != "ALL":
            st = stance.upper()
            if st == "STANCE_ONLY":
                query = query.filter(
                    or_(
                        Move.hit_level == "s",
                        Move.stance_context.isnot(None),
                        Move.properties.any(MoveProperty.property_type.ilike("%stance%")),
                    )
                )
            elif st == "NEUTRAL_ONLY":
                query = query.filter(
                    and_(
                        Move.hit_level != "s",
                        Move.stance_context.is_(None),
                        ~Move.properties.any(MoveProperty.property_type.ilike("%stance%")),
                    )
                )
            else:
                query = query.filter(Move.stance_context.ilike(f"%{stance}%"))

        # Verification Status
        if verification_status and verification_status.upper() != "ALL":
            query = query.filter(Move.verification_status == verification_status.upper())

        # Patch Version
        if patch_version and patch_version.upper() != "ALL":
            query = query.filter(Move.patch.has(GamePatch.version_number == patch_version))

        # Freeform Query Search
        if query_str:
            term = query_str.strip()
            query = query.filter(
                or_(
                    Move.name.ilike(f"%{term}%"),
                    Move.original_notation.ilike(f"%{term}%"),
                    Move.normalized_notation.ilike(f"%{term}%"),
                    Move.hit_level.ilike(f"%{term}%"),
                    Move.stance_context.ilike(f"%{term}%"),
                    Move.properties.any(MoveProperty.property_type.ilike(f"%{term}%")),
                )
            )

        total_count = query.count()
        raw_moves = query.order_by(Move.id.asc()).offset(offset).limit(limit).all()

        enriched = [cls.enrich_move(m) for m in raw_moves]
        return enriched, total_count

    @classmethod
    def get_summary_stats(cls, db: Session, character_slug: Optional[str] = None) -> MoveSummaryStats:
        query = db.query(Move)
        if character_slug:
            char = db.query(Character).filter(Character.slug == character_slug.lower()).first()
            if char:
                query = query.filter(Move.character_id == char.id)

        all_moves = query.all()
        total = len(all_moves)

        verified = sum(1 for m in all_moves if m.verification_status == "VERIFIED")
        verified_pct = round((verified / max(1, total)) * 100, 1)

        safe = sum(1 for m in all_moves if m.block_advantage is not None and m.block_advantage >= -9)
        unsafe = sum(1 for m in all_moves if m.block_advantage is not None and -14 <= m.block_advantage <= -10)
        launch = sum(1 for m in all_moves if m.block_advantage is not None and m.block_advantage <= -15)
        plus = sum(1 for m in all_moves if m.block_advantage is not None and m.block_advantage >= 1)

        heat = sum(
            1 for m in all_moves
            if any("heat" in p.property_type.lower() for p in m.properties)
        )
        homing = sum(
            1 for m in all_moves
            if any("homing" in p.property_type.lower() for p in m.properties)
        )
        pc = sum(
            1 for m in all_moves
            if any("power-crush" in p.property_type.lower() or "power_crush" in p.property_type.lower() for p in m.properties)
        )

        return MoveSummaryStats(
            total_moves=total,
            verified_count=verified,
            verified_percentage=verified_pct,
            safe_moves_count=safe,
            unsafe_moves_count=unsafe,
            launch_punishable_count=launch,
            plus_on_block_count=plus,
            heat_engagers_count=heat,
            homing_count=homing,
            power_crush_count=pc,
        )
