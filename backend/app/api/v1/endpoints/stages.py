from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.stage import Stage
from backend.app.schemas.stage import StageRead
from backend.app.services.matchup_analyzer import MatchupAnalyzerEngine

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
