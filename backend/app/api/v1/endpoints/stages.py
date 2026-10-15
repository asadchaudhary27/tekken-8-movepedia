from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.stage import Stage
from backend.app.models.character import Character
from backend.app.schemas.stage import StageRead
from backend.app.schemas.stage_strategy import StageStrategyReport
from backend.app.services.matchup_analyzer import MatchupAnalyzerEngine
from backend.app.services.stage_strategy_engine import StageStrategyEngine

router = APIRouter()


@router.get("", response_model=List[StageRead], summary="List all verified Tekken 8 stages")
def list_stages(
    has_walls: Optional[bool] = Query(None, description="Filter by presence of walls"),
    wall_break: Optional[bool] = Query(None, description="Filter by wall-break hazard"),
    floor_break: Optional[bool] = Query(None, description="Filter by floor-break hazard"),
    balcony_break: Optional[bool] = Query(None, description="Filter by balcony-break hazard"),
    search: Optional[str] = Query(None, description="Search by stage name or location"),
    db: Session = Depends(get_db)
):
    """
    Returns all verified Tekken 8 stage battlegrounds with their destructible hazards,
    boundary geometry, and transition zones.
    """
    query = db.query(Stage)

    if has_walls is not None:
        query = query.filter(Stage.has_walls == has_walls)
    if wall_break is not None:
        query = query.filter(Stage.wall_break == wall_break)
    if floor_break is not None:
        query = query.filter(Stage.floor_break == floor_break)
    if balcony_break is not None:
        query = query.filter(Stage.balcony_break == balcony_break)
    if search:
        query = query.filter(
            (Stage.name.ilike(f"%{search}%")) | (Stage.location.ilike(f"%{search}%"))
        )

    stages = query.order_by(Stage.id.asc()).all()
    results = []
    for s in stages:
        s_read = StageRead.model_validate(s)
        s_read.hazards = MatchupAnalyzerEngine.get_stage_hazards_list(s)
        results.append(s_read)
    return results


@router.get("/{stage_id}/strategy", response_model=StageStrategyReport, summary="Get stage-aware strategy and tactical recommendations")
def get_stage_strategy(
    stage_id: int,
    player_character_id: Optional[int] = Query(None, description="Selected player character ID"),
    player_slug: Optional[str] = Query(None, description="Selected player character slug"),
    opponent_character_id: Optional[int] = Query(None, description="Opponent character ID"),
    opponent_slug: Optional[str] = Query(None, description="Opponent character slug"),
    wall_position: Optional[str] = Query("OPEN", description="OPEN, NEAR_WALL, or CORNER"),
    heat_state: Optional[str] = Query("AVAILABLE", description="AVAILABLE, IN_HEAT, or SPENT"),
    db: Session = Depends(get_db)
):
    """
    Analyzes stage boundary geometry, wall positions, and destructible hazards for the selected
    character pair. Filters and categorizes midscreen combos, wall-carry routes, wall enders,
    wall breaks, floor breaks, balcony breaks, corner pressure, and flags unavailable mechanics.
    """
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stage ID {stage_id} not found."
        )

    player_char = None
    if player_character_id is not None:
        player_char = db.query(Character).filter(Character.id == player_character_id).first()
    elif player_slug:
        player_char = db.query(Character).filter(Character.slug == player_slug).first()

    if not player_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player character not found (ID: {player_character_id}, slug: '{player_slug}')."
        )

    opponent_char = None
    if opponent_character_id is not None:
        opponent_char = db.query(Character).filter(Character.id == opponent_character_id).first()
    elif opponent_slug:
        opponent_char = db.query(Character).filter(Character.slug == opponent_slug).first()

    return StageStrategyEngine.analyze_stage_strategy(
        db=db,
        stage=stage,
        player_char=player_char,
        opponent_char=opponent_char,
        wall_position=wall_position,
        heat_state=heat_state
    )


@router.get("/{stage_id_or_slug}", response_model=StageRead, summary="Get stage by ID or slug")
def get_stage(stage_id_or_slug: str, db: Session = Depends(get_db)):
    """
    Retrieves full details and mechanics for a specific Tekken 8 battleground.
    """
    if stage_id_or_slug.isdigit():
        stage = db.query(Stage).filter(Stage.id == int(stage_id_or_slug)).first()
    else:
        stage = db.query(Stage).filter(Stage.slug == stage_id_or_slug.lower()).first()

    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stage '{stage_id_or_slug}' not found."
        )

    s_read = StageRead.model_validate(stage)
    s_read.hazards = MatchupAnalyzerEngine.get_stage_hazards_list(stage)
    return s_read

