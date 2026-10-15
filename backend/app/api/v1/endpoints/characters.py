from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.schemas.character import CharacterResponse
from backend.app.core.errors import CharacterNotFoundException

router = APIRouter()


@router.get("", response_model=List[CharacterResponse], summary="List all Tekken 8 fighters")
def list_characters(
    archetype: Optional[str] = Query(None, description="Filter by category: Allies, Mishima, Rebels, Newcomers, etc."),
    is_dlc: Optional[bool] = Query(None, description="Filter by DLC status"),
    db: Session = Depends(get_db)
):
    query = db.query(Character)
    if archetype:
        query = query.filter(Character.archetype.ilike(f"%{archetype}%"))
    if is_dlc is not None:
        query = query.filter(Character.is_dlc == is_dlc)

    characters = query.order_by(Character.name.asc()).all()
    results = []
    for c in characters:
        res = CharacterResponse.model_validate(c)
        res.move_count = len(c.moves)
        results.append(res)
    return results


@router.get("/{slug}", response_model=CharacterResponse, summary="Get character by slug")
def get_character(slug: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.slug == slug.lower()).first()
    if not character:
        raise CharacterNotFoundException(slug)
    res = CharacterResponse.model_validate(character)
    res.move_count = len(character.moves)
    return res
