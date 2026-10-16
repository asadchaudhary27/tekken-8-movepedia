from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.search import GlobalSearchResponse
from backend.app.services.global_search_service import GlobalSearchService

router = APIRouter()


@router.get("", response_model=GlobalSearchResponse)
def global_search(
    q: str = Query(..., min_length=1, description="Search query string (fighter, move, frame, combo, or stage)"),
    category: Optional[str] = Query("ALL", description="Filter category: ALL, CHARACTER, MOVE, COMBO, STAGE"),
    limit: int = Query(10, ge=1, le=50, description="Max results per category"),
    db: Session = Depends(get_db),
):
    """
    Search across characters, moves, combos, stages, and frame advantage values in real-time.
    """
    return GlobalSearchService.search(
        db=db,
        query_str=q,
        category_filter=category,
        limit_per_category=limit,
    )
