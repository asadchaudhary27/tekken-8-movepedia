"""
Stage-Aware Strategy Engine for Tekken 8.
Evaluates stage boundary geometry, wall positions, destructible hazard availability,
and filters character combos across midscreen, wall-carry, wall-splat enders,
wall breaks, floor breaks, and balcony breaks.
Strict Data Integrity: Zero fabricated geometry or fake break mechanics.
"""

from typing import List, Optional, Dict, Any
import json
from sqlalchemy.orm import Session
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.models.combo_route import ComboRoute
from backend.app.schemas.stage import StageRead
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.combo import ComboRouteRead
from backend.app.schemas.stage_strategy import StageStrategyReport
from backend.app.services.matchup_analyzer import MatchupAnalyzerEngine


class StageStrategyEngine:
    """Core analytical service for stage-aware strategy and hazard-specific combo filtering."""

    @classmethod
    def analyze_stage_strategy(
        cls,
        db: Session,
        stage: Stage,
        player_char: Character,
        opponent_char: Optional[Character] = None,
        wall_position: Optional[str] = "OPEN",
        heat_state: Optional[str] = "AVAILABLE"
    ) -> StageStrategyReport:
        # 1. Fetch player's full combo repertoire
        all_combos = db.query(ComboRoute).filter(
            ComboRoute.character_id == player_char.id
        ).all()

        # 2. Evaluate stage boundaries and unavailable mechanics
        unavailable_warnings: List[str] = []
        is_infinite = not stage.has_walls

        if is_infinite:
            wall_status = "UNAVAILABLE (Infinite Stage)"
            unavailable_warnings.append(
                f"{stage.name} is an infinite battleground with no perimeter walls. "
                "Wall carries, wall-splats, and wall-combo enders are completely UNAVAILABLE."
            )
            unavailable_warnings.append(
                "Destructible environmental breaks (wall break, floor break, balcony break) do not exist."
            )
            corner_strat = (
                "No corners or boundaries exist on this stage. It is impossible to trap the opponent. "
                "Focus entirely on neutral spacing, whiff punishment, and max-damage midscreen juggles."
            )
            wall_positioning = (
                "Spacing is unbounded. Backward and lateral mobility are unrestricted; "
                "maintain Range 2 to 2.5 to bait whiffs without fear of being cornered."
            )
        else:
            wall_status = f"AVAILABLE ({stage.boundary_shape or 'Enclosed'} Walls, {stage.wall_distance or 'Standard 24m'})"

            if not stage.wall_break:
                unavailable_warnings.append(
                    f"Wall break is UNAVAILABLE on {stage.name} (reinforced boundary structure)."
                )
            if not stage.floor_break and not stage.floor_blast:
                unavailable_warnings.append(
                    f"Floor break/blast is UNAVAILABLE on {stage.name} (solid foundation)."
                )
            if not stage.balcony_break:
                unavailable_warnings.append(
                    f"Balcony break is UNAVAILABLE on {stage.name} (single enclosed tier)."
                )

            # Wall positioning and corner pressure based on conditions
            if wall_position == "CORNER":
                corner_strat = (
                    f"Opponent is trapped in the corner on {stage.name}. Enforce devastating wall pressure! "
                    "Use mid/low 50-50 mixups and homing checks. Any knockdown guarantees wall-combo enders."
                )
                wall_positioning = "Maintain suffocating close range (R1). Do not let the opponent side-step or tech roll out of the corner."
            elif wall_position == "NEAR_WALL":
                corner_strat = (
                    f"Near the wall on {stage.name}, standard launcher strings achieve wall splat. "
                    "Shorten combo fillers and transition immediately to high-damage wall enders."
                )
                wall_positioning = "Corner is within 1 to 2 dash lengths. Wall splat angles are wide; prioritize horizontal push attacks."
            else:
                corner_strat = (
                    f"On {stage.name}, utilize wall-carry routes with tornado tailspins to push the opponent "
                    f"across the {stage.wall_distance or '24m'} distance into perimeter walls."
                )
                wall_positioning = "Neutral midscreen starting position. Optimize carry distance over pure raw midscreen damage."

        # 3. Categorize verified combos based on stage mechanics
        midscreen_combos: List[ComboRouteRead] = []
        wall_carry_routes: List[ComboRouteRead] = []
        wall_combo_enders: List[ComboRouteRead] = []
        wall_break_routes: List[ComboRouteRead] = []
        floor_break_routes: List[ComboRouteRead] = []
        balcony_break_routes: List[ComboRouteRead] = []

        universal_count = 0
        stage_dep_count = 0

        for c in all_combos:
            # Check stage specificity
            if c.is_stage_dependent:
                stage_dep_count += 1
                if c.stage_id is not None and c.stage_id != stage.id:
                    # Combo is specific to a DIFFERENT stage; skip
                    continue
            else:
                universal_count += 1

            c_read = ComboRouteRead.model_validate(c)

            ctype = (c.combo_type or "MIDSCREEN").upper()

            # Midscreen combos always work (even on infinite stages)
            if ctype == "MIDSCREEN" or not c.uses_wall:
                midscreen_combos.append(c_read)

            # Wall carry routes (only viable if stage has walls)
            if (ctype == "WALL_CARRY" or c.uses_tornado) and stage.has_walls:
                wall_carry_routes.append(c_read)

            # Wall combo enders (only viable if stage has walls)
            if (ctype == "WALL_COMBO" or c.uses_wall) and stage.has_walls:
                wall_combo_enders.append(c_read)

            # Wall break routes
            if (ctype == "WALL_BREAK" or "wall-break" in (c.conditions_notes or "").lower()) and stage.wall_break:
                wall_break_routes.append(c_read)

            # Floor break routes
            if (ctype == "FLOOR_BREAK" or "floor-break" in (c.conditions_notes or "").lower()) and (stage.floor_break or stage.floor_blast):
                floor_break_routes.append(c_read)

            # Balcony break routes
            if (ctype == "BALCONY_BREAK" or "balcony-break" in (c.conditions_notes or "").lower()) and stage.balcony_break:
                balcony_break_routes.append(c_read)

        # 4. Parse verified geometry data if available
        geometry_data = None
        has_geometry = False
        if stage.geometry_data_json:
            try:
                geometry_data = json.loads(stage.geometry_data_json)
                has_geometry = bool(geometry_data and geometry_data.get("is_verified", False))
            except Exception:
                geometry_data = None
                has_geometry = False

        # 5. Build tactical summary
        tactical_parts = []
        if is_infinite:
            tactical_parts.append(
                f"{stage.name} heavily favors characters with strong neutral control, long pokes, and high-damage open-field juggles."
            )
        else:
            tactical_parts.append(
                f"{stage.name} ({stage.boundary_shape or 'Enclosed'}) creates high reward for wall-carry execution."
            )
            if stage.wall_break:
                tactical_parts.append("Wall break extensions provide massive round-ending burst damage.")
            if stage.floor_break or stage.floor_blast:
                tactical_parts.append("Downward spike combo enders trigger floor destruction for extended juggles.")
            if stage.balcony_break:
                tactical_parts.append("Balcony break drops the rival into lower tiers with guaranteed follow-up pressure.")

        # StageRead schema
        s_read = StageRead.model_validate(stage)
        s_read.hazards = MatchupAnalyzerEngine.get_stage_hazards_list(stage)

        return StageStrategyReport(
            stage=s_read,
            player_character=CharacterRead.model_validate(player_char),
            opponent_character=CharacterRead.model_validate(opponent_char) if opponent_char else None,
            geometry_available=has_geometry,
            geometry_data=geometry_data,
            layout_description=stage.layout_description or stage.notes or f"Standard {stage.boundary_shape or 'enclosed'} arena.",
            wall_distance=stage.wall_distance or ("None (Infinite)" if is_infinite else "Standard (24m)"),
            wall_availability_status=wall_status,
            midscreen_combos=midscreen_combos,
            wall_carry_routes=wall_carry_routes,
            wall_combo_enders=wall_combo_enders,
            wall_break_routes=wall_break_routes,
            floor_break_routes=floor_break_routes,
            balcony_break_routes=balcony_break_routes,
            wall_break_interaction=stage.wall_break_interaction,
            floor_break_interaction=stage.floor_break_interaction,
            balcony_break_interaction=stage.balcony_break_interaction,
            corner_pressure_strategy=corner_strat,
            wall_positioning_notes=wall_positioning,
            unavailable_mechanics_warning=unavailable_warnings,
            universal_combos_count=universal_count,
            stage_dependent_combos_count=stage_dep_count,
            tactical_summary=" ".join(tactical_parts),
            source="TekkenDocs / Stage Strategy Lab",
            patch_version="3.00.02"
        )

    @classmethod
    def filter_combos(
        cls,
        db: Session,
        character_id: Optional[int] = None,
        character_slug: Optional[str] = None,
        stage_id: Optional[int] = None,
        stage_slug: Optional[str] = None,
        combo_type: Optional[str] = None,
        requires_heat: Optional[bool] = None,
        requires_ch: Optional[bool] = None,
        difficulty: Optional[str] = None,
        stage_section: Optional[str] = None
    ) -> List[ComboRouteRead]:
        """Filters combos dynamically based on multi-faceted criteria."""
        query = db.query(ComboRoute)

        if character_id is not None:
            query = query.filter(ComboRoute.character_id == character_id)
        elif character_slug:
            query = query.join(Character).filter(Character.slug == character_slug)

        if stage_id is not None:
            # Match combos that either work on all stages (is_stage_dependent=False)
            # OR are specifically assigned to this stage_id
            query = query.filter(
                (ComboRoute.is_stage_dependent == False) | (ComboRoute.stage_id == stage_id)
            )
        elif stage_slug:
            stage_match = db.query(Stage).filter(Stage.slug == stage_slug).first()
            if stage_match:
                query = query.filter(
                    (ComboRoute.is_stage_dependent == False) | (ComboRoute.stage_id == stage_match.id)
                )

        if combo_type and combo_type.upper() != "ALL":
            query = query.filter(ComboRoute.combo_type == combo_type.upper())

        if requires_heat is not None:
            query = query.filter(ComboRoute.uses_heat == requires_heat)

        if requires_ch is not None:
            query = query.filter(ComboRoute.requires_counter_hit == requires_ch)

        if difficulty and difficulty.upper() != "ALL":
            query = query.filter(ComboRoute.difficulty == difficulty.upper())

        if stage_section and stage_section.upper() != "ALL":
            query = query.filter(ComboRoute.stage_section.ilike(f"%{stage_section}%"))

        combos = query.order_by(ComboRoute.total_damage.desc()).all()
        return [ComboRouteRead.model_validate(c) for c in combos]
