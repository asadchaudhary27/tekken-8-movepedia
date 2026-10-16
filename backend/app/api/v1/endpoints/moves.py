from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.schemas.move import MoveResponse, MoveSummaryStats
from backend.app.services.move_explorer_service import MoveExplorerService
from backend.app.core.errors import MoveNotFoundException, CharacterNotFoundException

router = APIRouter()


@router.get("", response_model=List[MoveResponse], summary="List and filter moves with verified frame data")
def list_moves(
    character_id: Optional[int] = Query(None, description="Filter by character ID"),
    character_slug: Optional[str] = Query(None, description="Fighter slug, e.g. jin, kazuya, feng"),
    hit_level: Optional[str] = Query(None, description="Hit level: high, mid, low, special_mid, throw, stance, or ALL"),
    startup_min: Optional[int] = Query(None, description="Minimum startup frames (inclusive)"),
    startup_max: Optional[int] = Query(None, description="Maximum startup frames (inclusive)"),
    block_safety: Optional[str] = Query(None, description="SAFE (>= -9), UNSAFE (-10 to -14), LAUNCH_PUNISH (<= -15), PLUS (>= +1)"),
    punishability: Optional[str] = Query(None, description="SAFE, PUNISHABLE_10, PUNISHABLE_12, PUNISHABLE_14, LAUNCH_PUNISHABLE"),
    property_type: Optional[str] = Query(None, description="Filter by property: heat-engager, power-crush, homing, tornado, launcher, etc."),
    stance: Optional[str] = Query(None, description="ALL, STANCE_ONLY, NEUTRAL_ONLY, or specific stance name (e.g. ZEN)"),
    stance_filter: Optional[str] = Query(None, description="Alias for stance parameter"),
    verification_status: Optional[str] = Query(None, description="VERIFIED, EXPERIMENTAL, REPORTED, UNVERIFIED"),
    patch_version: Optional[str] = Query(None, description="Filter by patch version (e.g. 3.00.02)"),
    q: Optional[str] = Query(None, description="Search move name, notation, hit level, stance, or properties"),
    is_launcher: Optional[bool] = Query(None, description="Legacy launcher toggle"),
    min_damage: Optional[int] = Query(None, description="Legacy minimum damage filter"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Returns verified moves catalog with explicit frame data representation,
    punish recommendations, strategic defensive responses, and source/patch tracking.
    """
    # Legacy backwards compatibility mapping
    prop_filter = property_type
    if is_launcher and not prop_filter:
        prop_filter = "launcher"

    active_stance = stance or stance_filter

    moves, _ = MoveExplorerService.filter_moves(
        db=db,
        character_id=character_id,
        character_slug=character_slug,
        hit_level=hit_level,
        startup_min=startup_min,
        startup_max=startup_max,
        block_safety=block_safety,
        punishability=punishability,
        property_type=prop_filter,
        stance=active_stance,
        verification_status=verification_status,
        patch_version=patch_version,
        query_str=q,
        limit=limit,
        offset=offset,
    )

    if min_damage is not None:
        moves = [m for m in moves if (m.damage is not None and m.damage >= min_damage)]

    return moves


@router.get("/stats/summary", response_model=MoveSummaryStats, summary="Get frame safety and verification statistics")
def get_move_stats_summary(
    character_slug: Optional[str] = Query(None, description="Optional fighter slug to scope stats"),
    db: Session = Depends(get_db)
):
    """
    Returns aggregate counts for verified moves, safe on block moves,
    launch-punishable moves, and heat/homing tactical mechanics.
    """
    return MoveExplorerService.get_summary_stats(db=db, character_slug=character_slug)


@router.get("/{move_id}", response_model=MoveResponse, summary="Get single move detail with verified punish analysis")
def get_move(move_id: int, db: Session = Depends(get_db)):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise MoveNotFoundException(move_id)
    return MoveExplorerService.enrich_move(move)
