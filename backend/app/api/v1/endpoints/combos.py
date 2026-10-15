from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.schemas.combo import ComboRouteRead
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
    stage_section: Optional[str] = Query(None, description="Filter by stage section (e.g. Subway, Magma)"),
    db: Session = Depends(get_db)
):
    """
    Returns verified combo routes filtered by tactical classification (midscreen, wall carry,
    wall combo ender, wall break, floor break, balcony break), stage dependencies, Heat state,
    counter-hit starters, and execution difficulty. Zero guessed routes.
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
