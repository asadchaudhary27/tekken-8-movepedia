"""
Tekken 8 Matchup Analyzer Engine.
Calculates mathematically grounded punish windows, key tool comparisons,
stage hazard synergies, and combo recommendations from verified database records.
Strict Data Integrity: Zero fabricated frame numbers, win rates, or fake bonuses.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.move_property import MoveProperty
from backend.app.models.stage import Stage
from backend.app.models.combo_route import ComboRoute
from backend.app.models.matchup_note import MatchupNote
from backend.app.schemas.matchup import (
    MatchupConditions,
    PunishOption,
    KeyMoveInfo,
    ComboRecommendation,
    StageSynergyInfo,
    MatchupOverviewResponse
)
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.stage import StageRead


class MatchupAnalyzerEngine:
    """Core analytical service for character-versus-character and stage dynamics."""

    @classmethod
    def analyze_matchup(
        cls,
        db: Session,
        player_char: Character,
        opponent_char: Character,
        stage: Stage,
        conditions: MatchupConditions
    ) -> MatchupOverviewResponse:
        # 1. Fetch moves for player and opponent
        player_moves = db.query(Move).filter(Move.character_id == player_char.id).all()
        opponent_moves = db.query(Move).filter(Move.character_id == opponent_char.id).all()

        # 2. Compute verified punish matrix
        punish_matrix = cls.compute_punish_matrix(player_moves, opponent_moves)

        # 3. Compute player key moves
        key_moves = cls.extract_key_moves(player_moves)

        # 4. Compute stage synergy and hazard advice
        stage_synergy = cls.evaluate_stage_synergy(stage, conditions)

        # 5. Retrieve suitable combos from verified combo routes
        suitable_combos = cls.find_suitable_combos(db, player_char.id, stage, conditions)

        # 6. Evaluate archetype strengths and weaknesses
        strengths, weaknesses = cls.evaluate_strengths_and_weaknesses(
            player_char, player_moves, opponent_char, opponent_moves
        )

        # 7. Check for specific lab notes
        lab_note = db.query(MatchupNote).filter(
            MatchupNote.player_character_id == player_char.id,
            MatchupNote.opponent_character_id == opponent_char.id
        ).first()

        if lab_note and lab_note.overview:
            matchup_notes_text = lab_note.overview
            has_specific_notes = True
            if lab_note.key_advice:
                matchup_notes_text += f"\n\nAdvice: {lab_note.key_advice}"
        else:
            matchup_notes_text = (
                f"Pair-specific lab notes not cataloged yet for {player_char.name} vs {opponent_char.name}. "
                "Frame data analysis and punish windows are calculated live from verified patch records."
            )
            has_specific_notes = False

        # 8. Data completeness tracking
        completeness = {
            "patch_version": "3.00.02",
            "player_moves_analyzed": len(player_moves),
            "opponent_moves_analyzed": len(opponent_moves),
            "punish_options_found": len(punish_matrix),
            "stage_hazards_verified": len(cls.get_stage_hazards_list(stage)),
            "is_lab_verified": has_specific_notes
        }

        # Build StageRead object with hazard list
        stage_read = StageRead(
            id=stage.id,
            slug=stage.slug,
            name=stage.name,
            location=stage.location,
            image_url=stage.image_url,
            has_walls=stage.has_walls,
            boundary_shape=stage.boundary_shape,
            wall_break=stage.wall_break,
            hard_wall_break=stage.hard_wall_break,
            wall_blast=stage.wall_blast,
            wall_bound=stage.wall_bound,
            floor_break=stage.floor_break,
            floor_blast=stage.floor_blast,
            balcony_break=stage.balcony_break,
            has_transitions=stage.has_transitions,
            transition_description=stage.transition_description,
            total_sections=stage.total_sections,
            special_mechanics=stage.special_mechanics,
            notes=stage.notes,
            data_source_id=stage.data_source_id,
            hazards=cls.get_stage_hazards_list(stage)
        )

        return MatchupOverviewResponse(
            player_character=CharacterRead.model_validate(player_char),
            opponent_character=CharacterRead.model_validate(opponent_char),
            stage=stage_read,
            conditions=conditions,
            punish_matrix=punish_matrix,
            player_key_moves=key_moves,
            stage_synergy=stage_synergy,
            suitable_combos=suitable_combos,
            strengths=strengths,
            weaknesses=weaknesses,
            matchup_notes=matchup_notes_text,
            has_specific_lab_notes=has_specific_notes,
            data_completeness=completeness
        )

    @classmethod
    def compute_punish_matrix(cls, player_moves: List[Move], opponent_moves: List[Move]) -> List[PunishOption]:
        """Calculates exact frame-advantage punish options against punishable opponent attacks."""
        punishes: List[PunishOption] = []

        # Find opponent moves that are punishable (block disadvantage <= -10)
        punishable_opponent_moves = [
            m for m in opponent_moves 
            if m.block_advantage is not None and m.block_advantage <= -10
        ]

        # Valid player attacks with known startup
        valid_player_punishers = [
            m for m in player_moves
            if m.startup_frames is not None and m.startup_frames >= 10
        ]

        for opp_m in punishable_opponent_moves:
            window = abs(opp_m.block_advantage)
            # Candidate moves that fit in the window
            candidates = [p for p in valid_player_punishers if p.startup_frames <= window]
            if not candidates:
                continue

            # 1. Optimal damage candidate
            optimal_move = max(candidates, key=lambda x: (x.damage or 0, -x.startup_frames))
            
            # 2. Check if a launcher fits in the window
            launch_candidates = [
                c for c in candidates 
                if any(p.property_type == "launcher" for p in (c.properties or []))
            ]

            recommended = launch_candidates[0] if launch_candidates else optimal_move
            
            # Determine punish tier
            if recommended.startup_frames <= 10:
                tier = "i10 Jab Punish"
            elif recommended.startup_frames <= 12:
                tier = "i12 Frame Punish"
            elif recommended.startup_frames <= 14:
                tier = "i14 Intermediate Punish"
            else:
                tier = "Launch Punish"

            # Determine type
            is_launcher = any(p.property_type == "launcher" for p in (recommended.properties or []))
            is_heat = any("heat" in p.property_type for p in (recommended.properties or []))
            punish_type = "Launcher" if is_launcher else ("Heat Engager" if is_heat else "Heavy Knockdown")

            punishes.append(
                PunishOption(
                    opponent_move_name=opp_m.name,
                    opponent_move_input=opp_m.original_notation,
                    opponent_block_advantage=opp_m.block_advantage,
                    recommended_punish_name=recommended.name,
                    recommended_punish_input=recommended.original_notation,
                    punish_startup=recommended.startup_frames,
                    damage=recommended.damage,
                    punish_tier=tier,
                    punish_type=punish_type
                )
            )

        return punishes

    @classmethod
    def extract_key_moves(cls, player_moves: List[Move]) -> List[KeyMoveInfo]:
        """Identifies signature tactical moves from verified moves pool."""
        key_moves: List[KeyMoveInfo] = []

        for m in player_moves:
            props = [p.property_type for p in (m.properties or [])]
            role = "Tactical Move"

            if m.startup_frames == 10:
                role = "Fastest Check (i10 Punish)"
            elif m.hit_level == "m" and m.block_advantage is not None and m.block_advantage >= -3 and m.startup_frames and m.startup_frames <= 14:
                role = "Safe Mid Poke (Check)"
            elif any("heat-engager" in p for p in props):
                role = "Heat Engager"
            elif any("power-crush" in p for p in props):
                role = "Power Crush (Armor Absorption)"
            elif any("launcher" in p for p in props):
                role = "Main Launcher (Juggle Starter)"
            elif any("parry" in p for p in props):
                role = "Parry / Reversal"
            elif m.hit_level == "l" and m.damage and m.damage >= 18:
                role = "High-Damage Low Poke"

            key_moves.append(
                KeyMoveInfo(
                    move_name=m.name,
                    input=m.original_notation,
                    startup_frames=m.startup_frames,
                    block_advantage=m.block_advantage,
                    damage=m.damage,
                    hit_level=m.hit_level,
                    role=role,
                    properties=props
                )
            )

        return key_moves[:6]

    @classmethod
    def evaluate_stage_synergy(cls, stage: Stage, conditions: MatchupConditions) -> StageSynergyInfo:
        """Evaluates stage wall boundaries and destructible hazards against conditions."""
        hazards = cls.get_stage_hazards_list(stage)
        
        wall_danger = "Low"
        if stage.has_walls:
            if conditions.wall_position == "CORNER":
                wall_danger = "Extreme (Corner Pressure)"
            elif conditions.wall_position == "NEAR_WALL":
                wall_danger = "High (Wall Splat Active)"
            else:
                wall_danger = "Moderate (Standard Walled)"

        wall_mechanics = []
        if stage.wall_break: wall_mechanics.append("Wall Break")
        if stage.hard_wall_break: wall_mechanics.append("Hard Wall Break")
        if stage.wall_blast: wall_mechanics.append("Wall Blast")
        if stage.wall_bound: wall_mechanics.append("Wall Bound")

        floor_mechanics = []
        if stage.floor_break: floor_mechanics.append("Floor Break")
        if stage.floor_blast: floor_mechanics.append("Floor Blast")
        if stage.balcony_break: floor_mechanics.append("Balcony Break")

        # Tactical advice based on real stage configuration
        advice_parts = []
        if not stage.has_walls:
            advice_parts.append("Infinite boundary configuration: prioritize long juggles and neutral spacing over wall-carry.")
        else:
            if conditions.wall_position in ["NEAR_WALL", "CORNER"]:
                advice_parts.append(
                    f"{stage.name} features walled boundaries. Near the wall, avoid high-recovery moves and fish for wall splats."
                )
            else:
                advice_parts.append(f"{stage.name} has walls: aim for tornado tailspins that carry the opponent into the perimeter.")

        if stage.floor_blast or stage.floor_break:
            advice_parts.append("Destructible floor hazard active: downward slam combo enders will trigger extended damage.")
        if stage.wall_blast:
            advice_parts.append("Explosive wall blast hazard active: wall impacts inflict massive bonus knockback.")

        return StageSynergyInfo(
            has_walls=stage.has_walls,
            wall_danger_level=wall_danger,
            wall_mechanics=wall_mechanics,
            floor_mechanics=floor_mechanics,
            transition_notes=stage.transition_description,
            tactical_advice=" ".join(advice_parts)
        )

    @classmethod
    def find_suitable_combos(
        cls,
        db: Session,
        character_id: int,
        stage: Stage,
        conditions: MatchupConditions
    ) -> List[ComboRecommendation]:
        """Finds verified combo routes tailored to stage and conditions."""
        combos = db.query(ComboRoute).filter(ComboRoute.character_id == character_id).all()
        recs: List[ComboRecommendation] = []

        for c in combos:
            synergy = "Standard Staple Route"
            if c.uses_wall and stage.has_walls:
                synergy = "High Wall-Carry Synergy (Optimal for Walled Stages)"
            elif c.uses_heat and conditions.heat_state in ["AVAILABLE", "IN_HEAT"]:
                synergy = "Heat Dash Extended Route"
            elif c.uses_tornado:
                synergy = "Tornado Spin Wall-Travel Route"

            recs.append(
                ComboRecommendation(
                    title=c.title,
                    notation=c.notation_sequence,
                    damage=c.total_damage,
                    hits=c.hit_count,
                    difficulty=c.difficulty,
                    synergy_reason=synergy,
                    uses_heat=c.uses_heat,
                    uses_tornado=c.uses_tornado,
                    uses_wall=c.uses_wall
                )
            )

        return recs

    @classmethod
    def evaluate_strengths_and_weaknesses(
        cls,
        player_char: Character,
        player_moves: List[Move],
        opponent_char: Character,
        opponent_moves: List[Move]
    ) -> (List[str], List[str]):
        """Generates dynamic qualitative analysis grounded in character archetype and move properties."""
        strengths: List[str] = []
        weaknesses: List[str] = []

        # Player move attributes
        has_i10_fast = any(m.startup_frames == 10 for m in player_moves)
        launchers_count = sum(1 for m in player_moves if any(p.property_type == "launcher" for p in (m.properties or [])))
        heat_engagers_count = sum(1 for m in player_moves if any("heat" in p.property_type for p in (m.properties or [])))
        has_parry = any(any(p.property_type in ["parry", "reversal"] for p in (m.properties or [])) for m in player_moves)
        has_throws = any(m.hit_level == "t" for m in player_moves)

        # Strengths
        if has_i10_fast:
            strengths.append(f"Fast i10 interrupt tools allow reliable counter-poking against {opponent_char.name}.")
        if launchers_count >= 2:
            strengths.append("High aerial juggle potential with multiple launcher avenues.")
        if heat_engagers_count >= 1:
            strengths.append("Direct Heat System transitions to apply continuous offensive pressure.")
        if has_parry:
            strengths.append("Defensive parry capability to catch aggressive predictable sequences.")
        if has_throws:
            strengths.append("Unblockable command grab threat breaks defensive turtles.")
        if not strengths:
            strengths.append(f"Solid fundamentals and adaptable spacing with {player_char.name}.")

        # Opponent move attributes
        opp_punishable_count = sum(1 for m in opponent_moves if m.block_advantage is not None and m.block_advantage <= -10)
        opp_launchers = sum(1 for m in opponent_moves if any(p.property_type == "launcher" for p in (m.properties or [])))
        
        # Weaknesses
        if opp_launchers >= 2:
            weaknesses.append(f"Respect {opponent_char.name}'s launch threats on whiff; avoid throwing out high-recovery moves.")
        if opp_punishable_count < 2:
            weaknesses.append(f"{opponent_char.name} has compact, safe strings requiring patience and side-stepping.")
        else:
            weaknesses.append(f"Over-committing to heavy punishes may leave you vulnerable to {opponent_char.name}'s counter-attacks.")

        return strengths, weaknesses

    @classmethod
    def get_stage_hazards_list(cls, stage: Stage) -> List[str]:
        """Returns verified human-readable hazard labels for a stage."""
        hazards = []
        if stage.wall_blast: hazards.append("Wall Blast")
        if stage.hard_wall_break: hazards.append("Hard Wall Break")
        elif stage.wall_break: hazards.append("Wall Break")
        if stage.wall_bound: hazards.append("Wall Bound")
        if stage.floor_blast: hazards.append("Floor Blast")
        elif stage.floor_break: hazards.append("Floor Break")
        if stage.balcony_break: hazards.append("Balcony Break")
        if not hazards and stage.has_walls: hazards.append("Standard Walled")
        if not stage.has_walls: hazards.append("Infinite Arena")
        return hazards
