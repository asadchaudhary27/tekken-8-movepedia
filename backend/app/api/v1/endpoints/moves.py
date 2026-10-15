from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.schemas.move import MoveResponse
from backend.app.core.errors import MoveNotFoundException, CharacterNotFoundException

router = APIRouter()


@router.get("", response_model=List[MoveResponse], summary="List moves with optional filters")
def list_moves(
    character_slug: Optional[str] = Query(None, description="Fighter slug, e.g. jin, kazuya, feng"),
    hit_level: Optional[str] = Query(None, description="Hit level: h, m, l, sm, etc."),
    is_launcher: Optional[bool] = Query(None, description="Filter for launcher moves"),
    min_damage: Optional[int] = Query(None, description="Minimum damage"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Move)

    if character_slug:
        char = db.query(Character).filter(Character.slug == character_slug.lower()).first()
        if not char:
            raise CharacterNotFoundException(character_slug)
        query = query.filter(Move.character_id == char.id)

    if hit_level:
        query = query.filter(Move.hit_level.ilike(f"%{hit_level}%"))

    if min_damage is not None:
        query = query.filter(Move.damage >= min_damage)

    moves = query.offset(offset).limit(limit).all()
    return moves


@router.get("/{move_id}", response_model=MoveResponse, summary="Get single move detail")
def get_move(move_id: int, db: Session = Depends(get_db)):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise MoveNotFoundException(move_id)
    return move
