from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.models.combo_route import ComboRoute
from backend.app.schemas.combo import ComboRouteRead, ComboBenchmarkComparison
from backend.app.schemas.combo_compatibility import (
    ComboRecommendationReport,
    DamageCalculationRequest,
    DamageCalculationResult,
)
from backend.app.services.stage_strategy_engine import StageStrategyEngine
from backend.app.services.combo_compatibility_engine import ComboCompatibilityEngine

router = APIRouter()


@router.get("", response_model=List[ComboRouteRead], summary="Filter and list verified combo routes")
def list_combos(
    character_id: Optional[int] = Query(None, description="Filter by character ID"),
    character_slug: Optional[str] = Query(None, description="Filter by character slug"),
    stage_id: Optional[int] = Query(None, description="Filter by stage ID or compatibility"),
    stage_slug: Optional[str] = Query(None, description="Filter by stage slug"),
    combo_type: Optional[str] = Query(None, description="MIDSCREEN, WALL_CARRY, WALL_COMBO, WALL_BREAK, FLOOR_BREAK, BALCONY_BREAK, or ALL"),
    requires_heat: Optional[bool] = Query(None, description="Filter by Heat requirement"),
    requires_ch: Optional[bool] = Query(None, description="Filter by Counter-Hit requirement"),
    difficulty: Optional[str] = Query(None, description="EASY, MEDIUM, HARD, OPTIMAL, or ALL"),
    launcher_type: Optional[str] = Query(None, description="NORMAL_HIT, COUNTER_HIT, LAUNCHER, PUNISH, etc."),
    min_damage: Optional[int] = Query(None, description="Minimum scaled damage threshold"),
    max_damage: Optional[int] = Query(None, description="Maximum scaled damage threshold"),
    uses_wall: Optional[bool] = Query(None, description="Filter by wall interaction requirement"),
    uses_tornado: Optional[bool] = Query(None, description="Filter by tornado spin requirement"),
    is_stage_dependent: Optional[bool] = Query(None, description="Filter by stage dependency"),
    required_stance: Optional[str] = Query(None, description="Filter by required stance (e.g. ZEN, SENTAI)"),
    verification_status: Optional[str] = Query(None, description="VERIFIED, EXPERIMENTAL, REPORTED, UNVERIFIED"),
    target_hurtbox_class: Optional[str] = Query(None, description="UNIVERSAL, MALE_STANDARD, FEMALE_COMPACT, BIG, BEARS"),
    stage_section: Optional[str] = Query(None, description="Filter by stage section (e.g. Subway, Magma)"),
    q: Optional[str] = Query(None, description="Search starter, title, or notation"),
    db: Session = Depends(get_db)
):
    """
    Returns verified combo routes filtered by tactical classification, stage dependencies,
    starter type, damage range, stance requirements, Heat state, and execution difficulty. Zero guessed routes.
    """
    return StageStrategyEngine.filter_combos(
        db=db,
        character_id=character_id,
        character_slug=character_slug,
        stage_id=stage_id,
        stage_slug=stage_slug,
        combo_type=combo_type,
        requires_heat=requires_heat,
        requires_ch=requires_ch,
        difficulty=difficulty,
        launcher_type=launcher_type,
        min_damage=min_damage,
        max_damage=max_damage,
        uses_wall=uses_wall,
        uses_tornado=uses_tornado,
        is_stage_dependent=is_stage_dependent,
        required_stance=required_stance,
        verification_status=verification_status,
        target_hurtbox_class=target_hurtbox_class,
        stage_section=stage_section,
        query_str=q,
    )


@router.get(
    "/recommendations",
    response_model=ComboRecommendationReport,
    summary="Get 10-category character-specific combo recommendations with hurtbox compatibility"
)
def get_combo_recommendations(
    player_id: Optional[int] = Query(None, description="Player character ID"),
    player_slug: Optional[str] = Query(None, description="Player character slug"),
    opponent_id: Optional[int] = Query(None, description="Opponent character ID"),
    opponent_slug: Optional[str] = Query(None, description="Opponent character slug"),
    stage_id: Optional[int] = Query(None, description="Optional stage ID"),
    stage_slug: Optional[str] = Query(None, description="Optional stage slug"),
    wall_position: Optional[str] = Query("OPEN", description="OPEN, NEAR_WALL, WALL_SPLATTED"),
    heat_state: Optional[str] = Query("AVAILABLE", description="AVAILABLE, ACTIVE, DEPLETED"),
    db: Session = Depends(get_db)
):
    """
    Returns data-driven combo recommendations tailored to the selected player character,
    opponent character hurtbox profile (MALE_STANDARD, FEMALE_COMPACT, BIG, BEARS),
    and stage conditions. Combos are sorted into 10 analytical categories with 5-tier ranked
    compatibility status and verified Tekken 8 juggle damage scaling breakdown.
    """
    # Resolve player character
    player_query = db.query(Character)
    if player_id:
        player_char = player_query.filter(Character.id == player_id).first()
    elif player_slug:
        player_char = player_query.filter(Character.slug == player_slug.lower()).first()
    else:
        player_char = player_query.first()

    if not player_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player character not found."
        )

    # Resolve opponent character
    opp_query = db.query(Character)
    if opponent_id:
        opp_char = opp_query.filter(Character.id == opponent_id).first()
    elif opponent_slug:
        opp_char = opp_query.filter(Character.slug == opponent_slug.lower()).first()
    else:
        # Default opponent: pick second character or different character
        opp_char = opp_query.filter(Character.id != player_char.id).first()
        if not opp_char:
            opp_char = player_char

    if not opp_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent character not found."
        )

    # Resolve stage
    stage = None
    if stage_id:
        stage = db.query(Stage).filter(Stage.id == stage_id).first()
    elif stage_slug:
        stage = db.query(Stage).filter(Stage.slug == stage_slug.lower()).first()

    return ComboCompatibilityEngine.generate_recommendations(
        db=db,
        player_character=player_char,
        opponent_character=opp_char,
        stage=stage,
        wall_position=wall_position or "OPEN",
        heat_state=heat_state or "AVAILABLE",
    )


@router.post(
    "/calculate-damage",
    response_model=DamageCalculationResult,
    summary="Compute hit-by-hit aerial damage scaling (Tekken 8 scaling formula)"
)
def calculate_combo_damage(
    payload: DamageCalculationRequest
):
    """
    Computes hit-by-hit aerial damage scaling following verified Tekken 8 mechanics:
      Hit 1: 100% (120% if counter-hit starter)
      Hit 2: 70%
      Hit 3: 50%
      Hit 4: 40%
      Hit 5+: 30% floor
    Contrasts scaled result against blind raw summation.
    """
    return ComboCompatibilityEngine.calculate_scaled_damage(
        hits=payload.hits,
        is_counter_hit=payload.is_counter_hit,
        tested_damage=payload.tested_damage,
        damage_type=payload.damage_type,
        calculation_method=payload.calculation_method,
    )


@router.get(
    "/benchmark/compare",
    response_model=ComboBenchmarkComparison,
    summary="Side-by-side benchmark comparison of two combo routes"
)
def benchmark_compare_combos(
    combo_a_id: int = Query(..., description="ID of first combo route (e.g. P1)"),
    combo_b_id: int = Query(..., description="ID of second combo route (e.g. P2)"),
    db: Session = Depends(get_db)
):
    combo_a = db.query(ComboRoute).filter(ComboRoute.id == combo_a_id).first()
    combo_b = db.query(ComboRoute).filter(ComboRoute.id == combo_b_id).first()

    if not combo_a or not combo_b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both combo routes could not be found."
        )

    read_a = ComboRouteRead.model_validate(combo_a)
    if combo_a.character:
        read_a.character_name = combo_a.character.name
    read_b = ComboRouteRead.model_validate(combo_b)
    if combo_b.character:
        read_b.character_name = combo_b.character.name

    dmg_diff = combo_a.total_damage - combo_b.total_damage
    hit_diff = combo_a.hit_count - combo_b.hit_count
    dph_a = round(combo_a.total_damage / max(1, combo_a.hit_count), 2)
    dph_b = round(combo_b.total_damage / max(1, combo_b.hit_count), 2)

    # Assess direct comparability
    notes = []
    is_comparable = True

    same_ch = (combo_a.requires_counter_hit == combo_b.requires_counter_hit)
    if not same_ch:
        is_comparable = False
        notes.append("Asymmetric starter: One route requires Counter-Hit (CH) while the other is a Normal Hit starter.")

    same_wall = (combo_a.uses_wall == combo_b.uses_wall)
    if not same_wall:
        is_comparable = False
        notes.append("Stage difference: One route relies on Wall Splat/Combo while the other is open midscreen.")

    same_heat = (combo_a.uses_heat == combo_b.uses_heat)
    if not same_heat:
        notes.append("Resource delta: One route consumes Heat resource while the other is meterless.")

    if is_comparable:
        comp_summary = "Directly comparable: Both routes share compatible starter properties and neutral conditions."
    else:
        comp_summary = "Conditional divergence: " + " ".join(notes)

    # Practicality comparison
    diff_order = {"EASY": 1, "MEDIUM": 2, "HARD": 3, "OPTIMAL": 4}
    rank_a = diff_order.get((combo_a.difficulty or "MEDIUM").upper(), 2)
    rank_b = diff_order.get((combo_b.difficulty or "MEDIUM").upper(), 2)

    char_a_name = read_a.character_name or "Route 1"
    char_b_name = read_b.character_name or "Route 2"

    if rank_a < rank_b:
        pract = f"{char_a_name} is easier to execute consistently ({combo_a.difficulty}) than {char_b_name} ({combo_b.difficulty})."
    elif rank_a > rank_b:
        pract = f"{char_b_name} offers easier execution ({combo_b.difficulty}) compared to {char_a_name} ({combo_a.difficulty})."
    else:
        pract = f"Both routes feature equivalent execution difficulty ({combo_a.difficulty})."

    return ComboBenchmarkComparison(
        combo_a=read_a,
        combo_b=read_b,
        damage_difference=dmg_diff,
        hit_difference=hit_diff,
        damage_per_hit_a=dph_a,
        damage_per_hit_b=dph_b,
        is_directly_comparable=is_comparable,
        comparability_notes=comp_summary,
        practicality_comparison=pract
    )


@router.get(
    "/{combo_id}",
    response_model=ComboRouteRead,
    summary="Get verified combo route details by ID"
)
def get_combo_by_id(
    combo_id: int,
    db: Session = Depends(get_db)
):
    combo = db.query(ComboRoute).filter(ComboRoute.id == combo_id).first()
    if not combo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Combo route with ID {combo_id} not found."
        )
    read_obj = ComboRouteRead.model_validate(combo)
    if combo.character:
        read_obj.character_name = combo.character.name
    return read_obj

