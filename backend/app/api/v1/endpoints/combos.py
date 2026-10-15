from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.schemas.combo import ComboRouteRead
from backend.app.services.stage_strategy_engine import StageStrategyEngine

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
        stage_section=stage_section
    )
